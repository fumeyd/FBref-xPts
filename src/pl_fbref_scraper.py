import requests
import pandas as pd
from bs4 import BeautifulSoup

class fbref_scraper:
    def __init__(self):
        self.data = {}

    def scrape_fbref(self):
        url = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        self.get_gw(soup)
        self.get_score(soup)
        self.get_teams(soup)
        self.get_home_xg(soup)
        self.get_away_xg(soup)

        df = pd.DataFrame(data=self.data)
        df.drop(df[df.Score == ''].index, inplace=True)

        self.write_to_csv(df)

    def get_gw(self, soup):
        self.data["Wk"] = []
        cells = soup.find_all(attrs={"data-stat": "gameweek"})

        for cell in cells:
            text = cell.get_text()
            if text == 'Wk':
                continue
            
            self.data["Wk"].append(text)

    def get_teams(self, soup):
        self.data["Home"] = []
        self.data["Away"] = []
        home_cells = soup.find_all("td", attrs={"data-stat": "home_team"})
        away_cells = soup.find_all("td", attrs={"data-stat": "away_team"})

        for cell in home_cells:
            self.data["Home"].append(cell.get_text())

        for cell in away_cells:
            self.data["Away"].append(cell.get_text())

    def get_home_xg(self, soup):
        self.data["xG_home"] = []
        cells = soup.find_all("td", attrs={"data-stat": "home_xg"})

        for cell in cells:
            self.data["xG_home"].append(cell.get_text())

    def get_score(self, soup):
        self.data["Score"] = []
        cells = soup.find_all("td", attrs={"data-stat": "score"})

        for cell in cells:
            self.data["Score"].append(cell.get_text())

    def get_away_xg(self, soup):
        self.data["xG_away"] = []
        cells = soup.find_all("td", attrs={"data-stat": "away_xg"})

        for cell in cells:
            self.data["xG_away"].append(cell.get_text())

    def write_to_csv(self, df):
        file_path = 'raw_data/match_data_08_10_2024.csv'
        df.to_csv(file_path, index=False)