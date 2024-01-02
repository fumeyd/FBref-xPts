import numpy as np

class run_model:
    def __init__(self, match_data, teams):
        self.match_data = match_data
        self.team_df = teams

    def sim_match(self, xg_for, xg_against):
        if np.isnan(xg_for) or np.isnan(xg_against):
            return 'nan'

        xg_for_poisson = np.random.poisson(xg_for)
        xg_against_poisson = np.random.poisson(xg_against)

        if(xg_for_poisson > xg_against_poisson):
            return 3
        elif(xg_against_poisson > xg_for_poisson):
            return 0
        else:
            return 1
        
    def add_xPts(self, xPts, team):
        if team in self.team_df:
            self.team_df[team] += xPts
        else:
            self.team_df[team] = xPts

        return
        
    def main(self, row, simulations=10000):
        ## sim for home team
        home_total = 0
        for i in range(simulations):
            home_sim = self.sim_match(row.xG_home, row.xG_away)
            if home_sim != 'nan':
                home_total += home_sim

        home_xPts = home_total/simulations
        home_team = row.Home

        self.add_xPts(home_xPts, home_team)

        ## sim for away team
        away_total = 0
        for i in range(simulations):           
            away_sim = self.sim_match(row.xG_away, row.xG_home)
            if away_sim != 'nan':
                away_total += away_sim

        away_xPts = away_total/simulations
        away_team = row.Away

        self.add_xPts(away_xPts, away_team)

        return 