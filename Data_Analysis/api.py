#########################################
#   COMP90024 2023-S1 A2 Team 52        #
#   City: Melbourne                     #
#   Team members:                       #
#       Ganbayar Sukhbaatar - 1227274   #
#       ZHIQUAN LAI - 1118797           #
#       Mingyang Liu - 1113531          #
#       Jiahao Chen - 1118749           #
#       Lingling Yao - 1204405          #
#########################################

import requests, string
import pandas as pd
import couchdb

username = 'admin'
password = 'admin'
server = '172.26.130.118:80'
twitter_db = "twitter-geo"
mastodon_db = "mastodon_processed"

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

def conn():
    """
    Create db connection.
    """
    url = "http://" + username + ":" + password + "@" + server + "/"
    couch = couchdb.Server(url)
    return couch


def get_db(couch, name):
    """
    Given connectiona and db name, return db.
    """
    return couch[name]


def view_sum(db, req, group_level=1):
    """
    Getting the sum of all docs, group=True
    """
    res = {}
    view = db.view(req, group=True)
    for item in view:
        print(item.key, item.id, item.value)
        res[item.key] = item.value
    return {"res": res["total"]}


def twt_topic_dist(topic):
    try:
        res = {"med_inc": [], "uni_rate": [], "y12_rate": [], "part_rate": [], "tafe_rate": [], "emp_rate": []}
        count = 0
        sent_sum = 0
        for state in states_abbr.keys():
            temp = twt_state_topic_dist(topic, state)
            for k in temp.keys():
                v = temp[k]
                if k == "count":
                    count += v
                elif k == "avg_sent":
                    sent_sum += temp["count"] * v
                else:
                    res[k] += v
        res["count"] = count
        res["avg_sent"] = sent_sum / count if count != 0 else 0
        return res
    except Exception as e:
        return {"Error": e}


def mas_topic_view(topic):
    try:
        view_name = topic
        url = f"http://{username}:{password}@{server}/{mastodon_db}/_design/{view_name}/_view/{view_name}"
        params = {'group': 'false'}
        response = requests.get(url, params=params)
        data = response.json()
        return {topic: data["rows"][0]["value"]}
    except Exception as e:
        return {"Error": e}


def twt_state_topic_dist(topic, state):
    try:
        # Get sudo data
        sudo_gi_df = get_sudo_gi(state, df=True)

        # Get state view the topic
        view_df = twt_state_topic_view(topic, state, df=True)
        merged_df = pd.merge(sudo_gi_df, view_df, on='suburb')
        count_list = merged_df["count"].tolist()
        count = sum(count_list)
        sent_list = merged_df["avg_sent"].tolist()
        avg_sent = sum([x * y for x, y in zip(count_list, sent_list)]) / count if count != 0 else 0

        res = {"count": count, "avg_sent": avg_sent,
               "med_inc": merged_df["med_inc"].tolist(), "uni_rate": merged_df["uni_rate"].tolist(),
               "y12_rate": merged_df["y12_rate"].tolist(), "part_rate": merged_df["part_rate"].tolist(),
               "tafe_rate": merged_df["tafe_rate"].tolist(), "emp_rate": merged_df["emp_rate"].tolist()}
        return res
    except Exception as e:
        return {"Error": e}


def twt_state_topic_view(topic, state, df=False):
    try:
        view_name = f"{topic}_{states_abbr[state]}_suburb"
        url = f"http://{username}:{password}@{server}/{twitter_db}/_design/{view_name}/_view/{view_name}"
        params = {'group_level': 1}
        response = requests.get(url, params=params)
        data = response.json()
        res = []
        for row in data['rows']:
            loc = row['key']
            if loc == "":
                continue
            value = row['value']
            count = value['count']
            total = value['sum']
            avg_sentiment = total / count
            res.append([loc, count, avg_sentiment])

        column_titles = ["suburb", "count", "avg_sent"]
        if df:
            return pd.DataFrame(res, columns=column_titles)
        return pd.DataFrame(res, columns=column_titles).to_dict(orient='records')

    except Exception as e:
        return {"Error": e}


def get_sudo_gi(state, df=False):
    try:
        url = f"http://{username}:{password}@{server}/sudo_gi/_find"
        payload = {"limit": 10000,
                   "skip": 0,
                   "fields": ["suburb", "med_inc", "uni_rate", "y12_rate", "part_rate", "tafe_rate", "emp_rate",
                              "female_part", "male_part", "part_less"],
                   "selector": {"state": {"$eq": f"{state}"}}
                   }

        resp = requests.post(url, json=payload)
        data = resp.json()["docs"]
        if df:
            return pd.DataFrame(data)
        return data
    except Exception as e:
        return {"Error": e}


def get_sudo_avg(state):
    try:
        url = f"http://{username}:{password}@{server}/sudo_avg/_find"
        payload = {"limit": 10000,
                   "skip": 0,
                   "fields": ["state", "med_age", "med_week_inc"],
                   "selector": {"state": {"$eq": f"{state}"}}
                   }

        resp = requests.post(url, json=payload)
        data = resp.json()["docs"]
        return data[0]
    except Exception as e:
        return {"Error": e}

def get_hashtags_cnt(limit=10000):
    try:
        url = f"http://{username}:{password}@{server}/hashtags/_find"
        payload = {"limit": limit,
                   "skip": 0,
                   "fields": ["hashtag", "cnt"],
                   "selector": {"cnt": {"$gt": 0}},
                   "sort": [{"cnt": "desc"}]
                   }
        resp = requests.post(url, json=payload)
        data = resp.json()["docs"]
        return data
    except Exception as e:
        return {"Error": e}
    

def lang_view(db):
    try:
        if db == "twitter":
            url = f"http://{username}:{password}@{server}/{twitter_db}/_design/lang/_view/lang"
        elif db == "mastodon":
            url = f"http://{username}:{password}@{server}/{mastodon_db}/_design/lang/_view/lang"
        else:
            return {"Error": "Invalid db name"}
        params = {'group_level': 1}
        response = requests.get(url, params=params)
        data = response.json()
        return data['rows']
    except Exception as e:
        return {"Error": e}


def get_data_count(db):
    try:
        if db == "twitter":
            url = f"http://{username}:{password}@{server}/{twitter_db}"
        elif db == "mastodon":
            url = f"http://{username}:{password}@{server}/{mastodon_db}"
        else:
            return {"Error": "Invalid db name"}
        response = requests.get(url)
        data = response.json()
        return {"count": data['doc_count']}
    except Exception as e:
        return {"Error": e}


def twt_topic_count():
    try:
        url = f"http://{username}:{password}@{server}/topic_cnt/_find"
        payload = {"limit": 7,
                   "skip": 0,
                   "fields": ["topic", "cnt"],
                   "selector": {"cnt": {"$gt": 0}}
                   }
        resp = requests.post(url, json=payload)
        data = resp.json()["docs"]
        topics = []
        cnts = []
        for row in data:
            topics.append(row["topic"])
            cnts.append(row["cnt"])
        return {"topics": topics, "cnts": cnts}
    except Exception as e:
        return {"Error": e}

def get_topic_counts(sub_topic):
    res = twt_topic_count()
    topic = res["topics"]
    cnts = res["cnts"]
    dict = {}
    for i in range(len(topic)):
        dict[topic[i]] = cnts[i]
    m_c = dict[sub_topic]
    rest = dict["scotty"] + dict["cc"] + dict["nft"] + dict["porn"]
    data = {"counts": [m_c, rest]}
    return data

print(get_topic_counts("ukraine"))

def get_mas_topic_counts(sub_topic):
    # try:
    m_c = mas_topic_view(sub_topic)[sub_topic]
    rest = m_c
    rest += mas_topic_view("scotty")["scotty"]
    rest += mas_topic_view("ukraine")["ukraine"]
    rest += mas_topic_view("nft")["nft"]
    rest += mas_topic_view("cc")["cc"]
    data = {"counts": [m_c, rest]}
    return data

def prepare_dist(sub_topic):
    final_res = {}
    state_dist_dic = {}
    
    # prepare map
    res = []
    state_dist_dic = {}
    for state in states_abbr:
        tmp = {}
        tmp["state"] = string.capwords(state)
        tmp_avg = get_sudo_avg(state)
        tmp["mid_age"] = tmp_avg["med_age"]
        tmp["mid_week_inc"] = tmp_avg["med_week_inc"]

        state_dist_dic[state] = twt_state_topic_dist(sub_topic, state)
        tmp["cnt"] = state_dist_dic[state]["count"]
        tmp["sent"] = round(state_dist_dic[state]["avg_sent"], 3)
        res.append(tmp)

    final_res["map_data"] = res
    # prepare dist
    # AUS
    final_res["aus"] = twt_topic_dist(sub_topic)
    final_res["aus"]["sub"] = ", ".join([string.capwords(state) for state in states_abbr])
    # NSW
    final_res["nsw"] = state_dist_dic["new south wales"]
    final_res["nsw"]["sub"] = get_suburb(twt_state_topic_view(sub_topic, "new south wales"))
    # VIC
    final_res["vic"] = state_dist_dic["victoria"]
    final_res["vic"]["sub"] = get_suburb(twt_state_topic_view(sub_topic, "victoria"))
    # QSL
    final_res["qsl"] = state_dist_dic["queensland"]
    final_res["qsl"]["sub"] = get_suburb(twt_state_topic_view(sub_topic, "queensland"))
    # WA
    final_res["wa"] = state_dist_dic["western australia"]
    final_res["wa"]["sub"] = get_suburb(twt_state_topic_view(sub_topic, "western australia"))
    # SA
    final_res["sa"] = state_dist_dic["south australia"]
    final_res["sa"]["sub"] = get_suburb(twt_state_topic_view(sub_topic, "south australia"))
    # TAS
    final_res["tas"] = state_dist_dic["tasmania"]
    final_res["tas"]["sub"] = get_suburb(twt_state_topic_view(sub_topic, "tasmania"))
    # NT
    final_res["nt"] = state_dist_dic["northern territory"]
    final_res["nt"]["sub"] = get_suburb(twt_state_topic_view(sub_topic, "northern territory"))
    # ACT
    final_res["act"] = state_dist_dic["australian capital territory"]
    final_res["act"]["sub"] = get_suburb(twt_state_topic_view(sub_topic, "australian capital territory"))

    return final_res

def get_suburb(data):
    """
    Getting the suburb name from given list of dic.
    """
    res = ""
    for item in data:
        res += string.capwords(item["suburb"]) + ", "
    return res

