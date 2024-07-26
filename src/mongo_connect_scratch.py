import mongo_connect_utils as mc
import redis_connect_utils as rc
import ast
import csv
import math 

def main():
    mongo_conn = mc.mongoConnect()
    mongo_conn.startConnection()

    mongo_conn.set_last_gameweek({"tag" : "latest_gw"}, {"gameweek" : 28})
    # redis_conn = rc.redisConnect()
    # redis_conn.startConnection()

    # x = redis_conn.getAll()
    # unidict = {k.decode('utf8'): float(v.decode('utf8')) for k, v in x.items()}
    # print(x)

    # print(mongo_conn.get_last_gameweek())
    # client = mongo_conn.client
    # db = mongo_conn.client["teams-xPts-0"]
    # coll = db["xPts"]


    # doc = coll["gameweek_watermark"]
    # result = doc.find_one({"tag" : "latest_gw"})

    # print(result['gameweek'])
    # with open("raw_data/teams.csv", encoding='utf-8-sig') as csv_file:
    #     data = csv.reader(csv_file)
    #     test = {}
    #     for row in data:
    #         team = row[0]
    #         query = {"team" : team}
    #         result = mongo_conn.mongoQuery(query)
    #         test[team] = result['xPts']

    #     redis_conn.put(test)


    # return        

    # doc_to_update = {"team": "Arsenal"}
    # update = {"$set" : {"xPts" : 49.39}}

    # result = conn.collection.update_one(doc_to_update, update)
    # conn.initDatabase()
    # with open("raw_data/league_table_14_02_24.csv", encoding='utf-8-sig') as csv_file:
    #         data = csv.reader(csv_file)
    #         test = {}
    #         for row in data:
    #             test[row[1]] = row[len(row) - 1]
    #         print(test)
    # conn = rc.redisConnect()
    # conn.getConnDetails('config/redis_conn.json')
    # conn.startConnection()
    # conn.put({"Arsenal": 47.39})
    
    # ans = conn.get("Arsenal")
    # return ans

if __name__ == "__main__":
    main(); 