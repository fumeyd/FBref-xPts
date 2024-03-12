from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://fumeyd:fp0t5nE7kV0DwEO8@xpts-cluster-0.ly52h2x.mongodb.net/"

class mongoConnect:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None

    def startConnection(self): 
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.testConnection()

        self.db = self.client["teams-xPts-0"]
        self.collection = self.db["xPts"]

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
    
    def mongoInsert(self, data):
        if type(data) is list:
            res = self.collection.insert_many(data)
        else:
            res = self.collection.insert_one(data)
        return res
    
    def mongoUpdate(self, oldData, newData): 
        newQuery = {"$set" : newData}

        self.collection.update_one(oldData, newQuery, upsert=True)

    def mongoQuery(self, query):
        doc = self.collection.find_one(query)
        return query
    
    def mongoDelete(self, query):
        res = self.collection.delete_one(query)
        return res
    
    def mongoDrop(self):
        self.collection.drop()
