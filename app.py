from flask import Flask, render_template, request, session, jsonify, Response
from .google_scraper import GoogleScraper  # Assuming your scraper class exists
from io import StringIO, BytesIO
import boto3
import pandas as pd

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session management

df = pd.read_csv("google_map_scraper_accessKeys.csv")

AWS_ACCESS_KEY = df.loc[0, "Access key ID"]
AWS_SECRET_KEY = df.loc[0, "Secret access key"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scrape", methods=["POST"])
def scrape():

    session.pop("csv_data", None)
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"success": False})

    scraper = GoogleScraper()

    # Scrape reviews and store in session
    try:
        df = scraper.scrape_reviews(url)

        # Convert DataFrame to CSV and store it in session
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        session["csv_data"] = csv_buffer.getvalue()

        return jsonify({"success": True})
    except Exception as e:
        print(f"Error during scraping: {e}")
        return jsonify({"success": False})


@app.route("/scrape_status", methods=["GET"])
def scrape_status():
    # Check if CSV data is available in the session
    if "csv_data" in session:
        return jsonify({"ready": True})
    return jsonify({"ready": False})


@app.route("/download", methods=["GET"])
def download():
    # Get the CSV name from the user input
    csv_name = request.args.get("csv_name")

    # Retrieve the CSV data from the session
    csv_data = session.get("csv_data")

    if not csv_data:
        return "No CSV data available. Please scrape first."

    # Serve the CSV file as a downloadable file
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename={csv_name}.csv"},
    )


@app.route("/upload_s3", methods=["POST"])
def upload_s3():
    csv_name = request.args.get("csv_name")
    csv_data = session.get("csv_data")

    if not csv_data:
        return "No CSV data available. Please scrape first."

    # Initialize the S3 client (using environment variables or IAM role for credentials)
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
    )

    # Convert CSV string data into an in-memory file-like object using StringIO
    csv_buffer = BytesIO(csv_data.encode("utf-8"))

    # Specify the S3 bucket name and object key (filename in the bucket)
    bucket_name = "aws-etl-news"
    object_key = f"{csv_name}.csv"  # This will be the file name in S3

    try:
        # Upload the file to S3
        s3_client.upload_fileobj(csv_buffer, bucket_name, object_key)
        return jsonify(
            {"message": f"File uploaded successfully to S3 as {object_key}."}
        )
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
