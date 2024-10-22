import process_data as pd
import pl_fbref_scraper as fbref_scraper
import pl_site_table_scraper as table_scraper

def process():
    print("Scraping data from fbref... \n")
    scraper = fbref_scraper.fbref_scraper()
    scraper.scrape_fbref()

    print("Scraping league table from PL site... \n")
    scraper = table_scraper.pl_scraper()
    scraper = scraper.scrape_pl()

    csv = 'raw_data\match_data_08_10_2024.csv'

    process = pd.process_data(csv)
    print("Generating xPts... \n")
    test = process.do_run()
    return test

process()
