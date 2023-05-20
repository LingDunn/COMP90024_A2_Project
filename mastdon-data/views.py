import requests
import json

# CouchDB credentials and database info
username = 'admin'
password = 'admin'
server = '172.26.135.87:5984'
db_name = 'mastodon_processed'

def create_view(view_name, map_func):
    design_doc = {
        "_id": f"_design/{view_name}",
        "views": {
            view_name: {
                "map": map_func,
                "reduce": "_count"
            }
        }
    }
    design_doc_json = json.dumps(design_doc)
    url = f"http://{username}:{password}@{server}/{db_name}/_design/{view_name}"
    resp = requests.put(url, data=design_doc_json)
    print(resp.json())


def process(view_type, topic=None, sub_topic=None):
    if view_type == "topic":
        map_func = f'''function(doc){{
                            if(doc.topic.includes("{topic}")){{
                                emit(doc._id);
                            }}
                        }}'''
        create_view(f"{topic}", map_func)
    elif view_type == "sub_topic":
        map_func = f'''function(doc){{
                            if(doc.sub_topic.includes("{sub_topic}")){{
                                emit(doc._id);
                            }}
                        }}'''
        create_view(f"{sub_topic}", map_func)

def update(view_name):
    url = f"http://{username}:{password}@{server}/{db_name}/_design/{view_name}/_view/{view_name}"
    resp = requests.get(url)

topics = ['web3', 'politics', 'porn']
#for topic in topics:
#process("topic", topic=topics[0])
update('porn')

# sub_topics = ['cc', 'nft', 'scotty', 'ukraine']
# #for sub_topic in sub_topics:
# process("sub_topic", sub_topic=sub_topics[0])
