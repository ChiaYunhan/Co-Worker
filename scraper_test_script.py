from google_scraper import GoogleScraper


def main():
    scraper = GoogleScraper()

    # url = input("Please enter the Google Maps place URL: ")
    url = r"https://www.google.com/maps/place/BHub+Bouldering/@3.1003675,101.629364,17z/data=!4m16!1m9!3m8!1s0x31cc4b198acf5b35:0xe22ffd7c25489ee1!2sBHub+Bouldering!8m2!3d3.1003621!4d101.6319443!9m1!1b1!16s%2Fg%2F11vqnthfh1!3m5!1s0x31cc4b198acf5b35:0xe22ffd7c25489ee1!8m2!3d3.1003621!4d101.6319443!16s%2Fg%2F11vqnthfh1?entry=ttu&g_ep=EgoyMDI0MDkyOS4wIKXMDSoASAFQAw%3D%3D"
    # output_file = input('Enter output file name')
    output_file = "data/bhub23.csv"

    scraper.scrape_reviews(url, output_file=output_file)


if __name__ == "__main__":
    main()
