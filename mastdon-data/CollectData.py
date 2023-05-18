#
#app ID	        GNKm6QK1pHZALu7gtHmpd7cp1-qDVpCR7h1kTxzCGIE
#app seckey	    cQzZBUnuyVZiYEQqjWfXxBPI7zW5SHNrJNRKwitYYIU
#accsee token	c7BG0UO8NG5pSm1EM0WSyNX6_O7zhsHU22IhgYfRuJA
# https://aus.social/public/local
import os
import time
import requests
import json
import tqdm
# request on current data
websites=["https://aus.social/api/v1/timelines/public",
          "https://theblower.au/api/v1/timelines/public",
          "https://mastodon.au/api/v1/timelines/public"]

couchDB_address = 'http://admin:admin@172.26.135.87:5984/'
db_name = 'mastodon_data'

def get_data(url, max_id, limit, forward=False):
    if forward == False:
        params = {'local':True, 'max_id':max_id, 'limit':limit}
        resp = requests.get(url=url, params=params)
        try:
            data = resp.json()
            if len(data) == 0:
                print("url:",url,"null data",resp.text)
                return None, None
            oldest_id = data[-1]["id"]
        except:
            print(resp.text)
            print("retry in 100 sec")
            time.sleep(100)
            return None, None
        return data, oldest_id
    else:
        params = {'local':True, 'since_id':max_id, 'limit':limit}
        resp = requests.get(url=url, params=params)
        try:
            data = resp.json()
            if len(data) == 0:
                print("url:",url,"null data",resp.text)
                return None, None
            last_id = data[0]["id"]
        except:
            print(resp.text)
            print("retry in 100 sec")
            time.sleep(100)
            return None, None
        return data, last_id


# this function is to get historical data from matodon servers
def Get_Historical_data():
    last_ids = [None,None,None]
    if os.path.exists("oldest_id.txt"):
        last_id_file = open("oldest_id.txt", "r")
        # get last retrive ids
        if last_id_file.readline() != "":
            last_id_file.seek(0)
            for i in range(len(websites)):
                last_ids[i] = last_id_file.readline()[:-1]
                print(last_ids[i])
        last_id_file.close()

    # Collecting data
    num_data = 0
    while True:
        for x in range(len(websites)):
            data, last_id= get_data(websites[x], last_ids[x], 40)
            if data == None:
                continue
            num_data += 40
            last_ids[x] = last_id
            print("",websites[x],data[-1]["created_at"])
            for tweets in data:
                _id = tweets["id"]
                create_time = tweets["created_at"]
                lang = tweets["language"]
                content = tweets["content"]
                tags = tweets["tags"]
                fields = tweets["account"]["fields"]
                location = ''
                for f in fields:
                    if f['name'] == 'Location':
                        location = f['value']
                contents = {"create_time":create_time, "language":lang, "content":content, "tags":tags, "location":location}
                contents = json.dumps(contents)
                insert_data(db_name, _id, contents)
        #store current last id in disk
        last_id_file = open("oldest_id.txt", "w")
        for id in last_ids:
            last_id_file.writelines(id+'\n')
        last_id_file.close()
    last_id_file = open("oldest_id.txt", "w")
    for id in last_ids:
        last_id_file.writelines(id+'\n')

# update current database based on last id retrived
def update_data():
    last_ids = [None,None,None]
    if os.path.exists("latest_id.txt"):
        last_id_file = open("latest_id.txt", "r")
        # get last retrive ids
        if last_id_file.readline() != "":
            last_id_file.seek(0)
            for i in range(len(websites)):
                last_ids[i] = last_id_file.readline()[:-1]
                print(last_ids[i])
        last_id_file.close()

    while True:
        for x in range(len(websites)):
            data, last_id= get_data(websites[x], last_ids[x], 40, True)
            # No more new data coming in
            if data == None:
                print("",websites[x],"no more new data, wait 100 sec")
                time.sleep(100)
                continue
            last_ids[x] = last_id
            print("",websites[x],data[-1]["created_at"])
            for tweets in data:
                _id = tweets["id"]
                create_time = tweets["created_at"]
                lang = tweets["language"]
                content = tweets["content"]
                tags = tweets["tags"]
                fields = tweets["account"]["fields"]
                location = ''
                for f in fields:
                    if f['name'] == 'Location':
                        location = f['value']
                contents = {"create_time":create_time, "language":lang, "content":content, "tags":tags, "location":location}
                contents = json.dumps(contents)
                insert_data(db_name, _id, contents)
        #store current last id in disk
        last_id_file = open("latest_id.txt", "w")
        for id in last_ids:
            last_id_file.writelines(id+'\n')
        last_id_file.close()

def create_db(db_name):
    url = couchDB_address+db_name
    resp = requests.put(url=url)
    print(resp.text)

def insert_data(db_name, _id, data):
    param = {'new_edits':True}
    url = 'http://admin:admin@172.26.135.87:5984/' + db_name+ '/' + _id
    resp = requests.put(url=url, data=data, params=param)
    print(resp.text)

def get_all_data():
    url = couchDB_address+db_name+'/_all_docs'
    req = requests.get(url)
    data = req.json()
    data = data["rows"]
    all_id = [d["id"] for d in data]
    
if __name__ == '__main__':
    #Get_Historical_data()
    #update_data()
    get_all_data()