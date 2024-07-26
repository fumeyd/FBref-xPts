from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.write_concern import WriteConcern
from pymongo.read_concern import ReadConcern
from pymongo.read_preferences import ReadPreference

uri = "mongodb+srv://fumeyd:fp0t5nE7kV0DwEO8@xpts-cluster-0.ly52h2x.mongodb.net/"

class mongoConnect:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.gameweek_watermark = None

    def startConnection(self): 
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.testConnection()

        self.db = self.client["teams-xPts-0"]
        self.collection = self.db["xPts"]
        self.gameweek_watermark = self.db["gameweek_watermark"]

        return

    def testConnection(self):
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        return

    def initDatabase(self):
        if(self.client == None):
            self.startConnection()

        teams = self.createInitDict() 

        insert = self.mongoInsert(teams)

        return insert
    
    def createInitDict(self):
        teams = []

        teams_file = open("raw_data/teams.csv", "r").read().splitlines()
        for team in teams_file:
            team_dict = {}
            
            team_dict['team'] = team
            team_dict['xPts'] = 0
            teams.append(team_dict)

        return teams
    
    def get_last_gameweek(self):
        query = self.gameweek_watermark.find_one({"tag": "latest_gw"})

        return query["gameweek"]

    def set_last_gameweek(self, oldData, newData):
        def callback(session):
            newQuery = {"$set" : newData}
            self.gameweek_watermark.update_one(oldData, newQuery, upsert=True);

        try:
            with self.client.start_session() as session:
                session.with_transaction(
                    callback, 
                    read_concern=ReadConcern("local"), 
                    write_concern=WriteConcern("majority"),
                    read_preference=ReadPreference.PRIMARY
                )
        except Exception as e:
            return e

    def mongoInsert(self, data):
        def callback(session):
            if type(data) is list:
                res = self.collection.insert_many(data)
            else:
                res = self.collection.insert_one(data)
            return res
        
        try:
            with self.client.start_session() as session:
                session.with_transaction(
                    callback,
                    read_concern=ReadConcern("local"), 
                    write_concern=WriteConcern("majority"), 
                    read_preference=ReadPreference.PRIMARY,
                )
        except Exception as e:
            return e
    
    def mongoUpdate(self, oldData, newData): 
        def callback(session):
            newQuery = {"$set" : newData}
            self.collection.update_one(oldData, newQuery, upsert=True)

        try:
            with self.client.start_session() as session:
                session.with_transaction(
                    callback,
                    read_concern=ReadConcern("local"), 
                    write_concern=WriteConcern("majority"), 
                    read_preference=ReadPreference.PRIMARY,
                )
        except Exception as e:
            return e

    def mongoQuery(self, query):
        doc = self.collection.find_one(query)
        return doc
    
    def mongoDelete(self, query):
        def callback(session):
            res = self.collection.delete_one(query)
            return res
        
        try:
            with self.client.start_session() as session:
                session.with_transaction(
                    callback,
                    read_concern=ReadConcern("local"), 
                    write_concern=WriteConcern("majority"), 
                    read_preference=ReadPreference.PRIMARY,
                )
        except Exception as e:
            return e

    def mongoDrop(self):
        self.collection.drop()
