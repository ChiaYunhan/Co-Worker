// Handle form submission asynchronously for scraping
document.getElementById("scrape-form").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent normal form submission
    let url = document.getElementById("url").value;

    // Show loading spinner
    document.getElementById("loading").style.display = "block";

    // Hide download-upload form and status message initially
    document.getElementById("download-upload-form").style.display = "none";
    document.getElementById("status-message").style.display = "none"; 

    // Send an AJAX POST request to start scraping
    fetch('/scrape', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url })
    }).then(function(response) {
        return response.json();
    }).then(function(data) {
        if (data.success) {
            checkScrapeStatus();  // Check if scraping has completed
        } else {
            alert("Scraping failed, please try again.");
            document.getElementById("loading").style.display = "none"; // Hide loading spinner on failure
        }
    }).catch(function(error) {
        console.error("Error:", error);
        document.getElementById("loading").style.display = "none"; // Hide loading spinner on error
    });
});

// Function to check if scraping has completed
function checkScrapeStatus() {
    fetch('/scrape_status').then(function(response) {
        return response.json();
    }).then(function(data) {
        if (data.ready) {
            document.getElementById("loading").style.display = "none"; // Hide loading spinner
            document.getElementById("download-upload-form").style.display = "block"; // Show download-upload form
        } else {
            setTimeout(checkScrapeStatus, 2000); // Check every 2 seconds
        }
    });
}

// Handle the Download as CSV button click
document.getElementById("download-csv-btn").addEventListener("click", function() {
    let csvName = document.getElementById("csv_name").value;
    
    if (!csvName) {
        alert("Please enter a name for the CSV file.");
        return;
    }
    
    // Trigger download by redirecting to the /download endpoint with the csv_name
    window.location.href = '/download?csv_name=' + encodeURIComponent(csvName);
});

// Handle Upload to S3 logic
function uploadToS3() {
    // Get the CSV name from the input
    let csvName = document.getElementById("csv_name").value;

    if (!csvName) {
        alert("Please enter a CSV name before uploading to S3.");
        return;
    }

    // Show loading spinner (if any)
    document.getElementById("loading").style.display = "block";
    document.getElementById("status-message").style.display = "none"; // Hide previous status message

    // Send an AJAX POST request to upload the file to S3
    fetch('/upload_s3?csv_name=' + csvName, {
        method: 'POST'
    }).then(function(response) {
        return response.json();
    }).then(function(data) {
        document.getElementById("loading").style.display = "none"; // Hide loading spinner
        document.getElementById("status-message").style.display = "block"; // Show status message

        if (data.message) {
            document.getElementById("status-message").innerText = "Success: " + data.message;
            document.getElementById("status-message").style.color = "green";
        } else if (data.error) {
            document.getElementById("status-message").innerText = "Error: " + data.error;
            document.getElementById("status-message").style.color = "red";
        }
    }).catch(function(error) {
        console.error("Error:", error);
        document.getElementById("loading").style.display = "none"; // Hide loading spinner
        document.getElementById("status-message").style.display = "block"; // Show status message
        document.getElementById("status-message").innerText = "Error uploading to S3.";
        document.getElementById("status-message").style.color = "red";
    });
}

