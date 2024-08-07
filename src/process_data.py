import pandas as pd 
import generate_xPts as xPts

class process_data:
    def __init__(self, csv):
        self.df = self.csv_to_dataframe(csv) 
        self.teams = {}

    def csv_to_dataframe(self, csv):
        df = pd.read_csv(csv)

        return df
    
    def create_team_dataframe(self):
        team_df = pd.DataFrame(self.teams)

        return team_df
    
    def do_run(self):
        gen_xPts = xPts.run_model(self.df, self.teams)
        self.df.apply(gen_xPts.main, axis=1)
        gen_xPts.get_actual_pts()
        gen_xPts.persist_data()
        # gen_xPts.persist_to_mongo()
        # gen_xPts.persist_to_redis()

        return self.teams
