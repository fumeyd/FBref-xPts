import redis
import json

class redisConnect: 
    def __init__(self):
        self.client = None
        self.host = None
        self.password = None
        self.port = None

    def getConnDetails(self, file):
        details_file = open(file)
        data = json.load(details_file)["conn_details"]

        self.host = data["host"]
        self.password = data["password"]
        self.port = data["port"]

        details_file.close()
        return

    def testConnection(self): 
        try: 
            self.client.ping()
            print("Pinged your deployment. You successfully connected to Redis!")
        except Exception as e:
            print(e)

    def startConnection(self): 
        if self.client:
            return 
        
        if self.host == None or self.password == None or self.port == None:
            self.getConnDetails('config/redis_conn.json')

        self.client = redis.Redis(
            host=self.host,
            port=self.port,
            password=self.password
        )

        self.testConnection()
        
        return
    
    def put(self, dict):
        res = self.client.hset(
            "xPts", 
            mapping=dict
        )

        return 
    
    def get(self, key):
        query_result = self.client.hget("xPts", key)
        decoded = {k.decode('utf8'): float(v.decode('utf8')) for k, v in query_result.items()}
        
        return decoded

    def getAll(self):
        query_result = self.client.hgetall("xPts")
        decoded = {k.decode('utf8'): float(v.decode('utf8')) for k, v in query_result.items()}

        return decoded