import numpy as np
import mongo_connect_utils as mcu
import redis_connect_utils as rcu
import csv

class run_model:
    def __init__(self, match_data, teams):
        self.match_data = match_data
        self.team_df = teams
        self.mongo_client = None
        self.redis_client = None
        self.mconn = None
        self.actual_pts = None

    def init_connections(self):
        self.mconn = mcu.mongoConnect()
        self.mconn.startConnection()

        rconn = rcu.redisConnect()
        rconn.startConnection()

        self.mongo_client = self.mconn.client
        self.redis_client = rconn.client

        return

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
        # if not self.redis_client:
        #     self.init_connections()
        if team == 'nan':
            return 
        
        if team in self.team_df:
            self.team_df[team] += xPts
        else:
            self.team_df[team] = xPts

        return
    
    def get_actual_pts(self):
        if not self.actual_pts:
            with open("raw_data/league_table_14_02_24.csv", encoding='utf-8-sig') as csv_file:
                data = csv.reader(csv_file)
                points = {}
                for row in data:
                    points[row[1]] = row[len(row)-1]

                self.actual_pts = points
        return

    def persist_to_mongo(self):
        if not self.mongo_client:
            self.init_connections()

        for team in self.team_df:
            if team == 'nan' or type(team) is not str:
                continue
            
            query = {"team" : team}
            self.mconn.mongoUpdate(query, {"xPts" : self.team_df[team]})
            self.mconn.mongoUpdate(query, {"Pts" : int(self.actual_pts[team])})
        
        return
        
    def main(self, row, simulations=10000):
        ## sim for home team
        home_total = 0
        for i in range(simulations):
            home_sim = self.sim_match(row.xG_home, row.xG_away)
            if home_sim != 'nan':
                home_total += home_sim

        home_xPts = round(home_total/simulations, 3)
        home_team = row.Home

        self.add_xPts(home_xPts, home_team)

        ## sim for away team
        away_total = 0
        for i in range(simulations):           
            away_sim = self.sim_match(row.xG_away, row.xG_home)
            if away_sim != 'nan':
                away_total += away_sim

        away_xPts = round(away_total/simulations, 3)
        away_team = row.Away

        self.add_xPts(away_xPts, away_team)

        return 