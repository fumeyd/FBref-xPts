import requests
import pandas as pd
from bs4 import BeautifulSoup

class pl_scraper:
    def __init__(self):
        self.data = {}

    def scrape_pl(self):
        url = "https://www.premierleague.com/tables"
        response = requests.get(url)

        soup = BeautifulSoup(response.content, "html.parser")

        self.set_positions()
        self.set_teams(soup)
        self.set_added_data(soup)
        self.set_goals(soup)
        self.set_points(soup)

        df = pd.DataFrame(data=self.data)
        self.write_to_csv(df)

    def set_positions(self):
        self.data["Position"] = []
        for num in range(1,21):
            self.data["Position"].append(num)

    def set_teams(self, soup):
        self.data["Team"] = []
        team_rename_map = {"Manchester United": "Manchester Utd", 
                        "Newcastle United": "Newcastle Utd",
                        "Nottingham Forest": "Nott'ham Forest", 
                        "Wolverhampton Wanderers": "Wolves", 
                        "West Ham United": "West Ham", 
                        "Brighton and Hove Albion" : "Brighton", 
                        "Tottenham Hotspur": "Tottenham"
                            }
        
        cells = soup.find_all(attrs={"class": "league-table__team-name league-table__team-name--long long"})[0:20]

        for cell in cells: 
            team = cell.get_text()
            if team in team_rename_map:
                team = team_rename_map[team]
            self.data["Team"].append(team)

    def set_added_data(self, soup):
        self.data["GP"] = []
        self.data["W"] = []
        self.data["D"] = []
        self.data["L"] = []
        self.data["GD"] = []
        cells = soup.find_all(lambda tag: tag.name == 'td' and not tag.has_attr('class') and not tag.has_attr('colspan'))[0:100]

        for i in range(0, len(cells) - 1, 5):
            self.data["GP"].append(cells[i].get_text().strip())
            self.data["W"].append(cells[i+1].get_text().strip())
            self.data["D"].append(cells[i+2].get_text().strip())
            self.data["L"].append(cells[i+3].get_text().strip())
            self.data["GD"].append(cells[i+4].get_text().strip())

    def set_goals(self, soup):
        self.data["G"] = []
        self.data["GC"] = []
        cells = soup.find_all('td', attrs={"class": "hideSmall"})[0:40]

        for i in range(0, len(cells) - 1, 2):
            self.data["G"].append(cells[i].get_text())
            self.data["GC"].append(cells[i+1].get_text())

    def set_points(self, soup):
        self.data["Pts"] = []
        cells = soup.find_all('td', attrs={"class": "league-table__points points"})[0:20]

        for cell in cells:
            self.data["Pts"].append(cell.get_text())

    def write_to_csv(self, df):
        file_path = "raw_data/league_table_11_10_2024.csv"
        df.to_csv(file_path, index=False)
