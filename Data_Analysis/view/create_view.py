import requests
import json


# CouchDB credentials and database info
username = 'admin'
password = 'admin'
server = '172.26.135.87:5984'
db_name = 'twitter-geo'

states = ['new south wales',
          'victoria',
          'queensland',
          'south australia',
          'western australia',
          'tasmania',
          'northern territory',
          'australian capital territory'
          ]

states_abbr = {
    'new south wales': 'nsw',
    'victoria': 'vic',
    'queensland': 'qld',
    'south australia': 'sa',
    'western australia': 'wa',
    'tasmania': 'tas',
    'northern territory': 'nt',
    'australian capital territory': 'act'
}


def create_view(view_name, map_func, reduce_func="_stats"):
    design_doc = {
        "_id": f"_design/{view_name}",
        "views": {
            view_name: {
                "map": map_func,
                "reduce": f"{reduce_func}"
            }
        }
    }
    design_doc_json = json.dumps(design_doc)
    url = f"http://{username}:{password}@{server}/{db_name}/_design/{view_name}"
    resp = requests.put(url, data=design_doc_json)
    print(resp.json())


def process(view_type, suburb=False, topic=None, sub_topic=None):
    if suburb:
        for state in states:
            abbr = states_abbr[state]
            if view_type == "sentiment":
                map_func = f'''function(doc){{
                                   if(doc.state == "{state}" && doc.suburb != null && doc.sentiment != null){{
                                       emit(doc.suburb, doc.sentiment);
                                   }}
                               }}'''
                create_view(f"sentiment_{abbr}_suburb", map_func)
            elif view_type == "topic":
                map_func = f'''function(doc){{
                                   if(doc.state == "{state}" && doc.suburb != null
                                   && doc.sentiment != null && doc.topic.includes("{topic}")){{
                                       emit(doc.suburb, doc.sentiment);
                                   }}
                               }}'''
                create_view(f"{topic}_{abbr}_suburb", map_func)
            elif view_type == "sub_topic":
                map_func = f'''function(doc){{
                                   if(doc.state == "{state}" && doc.suburb != null
                                   && doc.sentiment != null && doc.sub_topic.includes("{sub_topic}")){{
                                       emit(doc.suburb, doc.sentiment);
                                   }}
                               }}'''
                create_view(f"{sub_topic}_{abbr}_suburb", map_func)
    else:
        if view_type == "sentiment":
            map_func = '''function(doc){
                              if(doc.state != null && doc.sentiment != null){
                                  emit(doc.state, doc.sentiment);
                              }
                          }'''
            create_view(f"sentiment_state", map_func)
        elif view_type == "topic":
            map_func = f'''function(doc){{
                               if(doc.state != null && doc.sentiment != null && doc.topic.includes("{topic}")){{
                                   emit(doc.state, doc.sentiment);
                               }}
                            }}'''
            create_view(f"{topic}_state", map_func)
        elif view_type == "sub_topic":
            map_func = f'''function(doc){{
                               if(doc.state != null && doc.sentiment != null && doc.sub_topic.includes("{sub_topic}")){{
                                   emit(doc.state, doc.sentiment);
                               }}
                            }}'''
            create_view(f"{sub_topic}_state", map_func)
        elif view_type == "lang":
            lang_reduce = '''function (keys, values, rereduce) {return sum(values)}'''
            map_func = f'''function(doc){{
                               if(doc.lang != null){{
                                   emit(doc.lang, 1);
                               }}
                            }}'''
            create_view("lang", map_func, lang_reduce)


# process("sentiment")
# process("sentiment", suburb=True)


# topics = ['web3', 'politics', 'porn']
# for topic in topics:
#     process("topic", topic=topic)
#     process("topic", suburb=True, topic=topic)


# sub_topics = ['cc', 'nft', 'scotty', 'ukraine']
# for sub_topic in sub_topics:
#     process("sub_topic", sub_topic=sub_topic)
#     process("sub_topic", suburb=True, sub_topic=sub_topic)


