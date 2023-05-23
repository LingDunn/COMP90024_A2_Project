import requests
import pandas as pd
from flask import Flask

app = Flask(__name__)

username = 'admin'
password = 'admin'
server = '172.26.135.87:5984'
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


@app.route('/')
def hello():
    return 'Hello'


# Given a topic, return distributions over all states
@app.route('/distribution/twitter/<string:topic>', methods=['GET'])
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


# Given a topic and a state, return distributions over the state
@app.route('/distribution/twitter/<string:topic>/<string:state>', methods=['GET'])
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


# Given a topic and a state, return topic_state_view
@app.route('/view/twitter/<string:topic>/<string:state>', methods=['GET'])
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


@app.route('/sudo/gi/<string:state>', methods=['GET'])
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


@app.route('/sudo/avg/<string:state>', methods=['GET'])
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


@app.route('/hashtags/<int:limit>', methods=['GET'])
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


@app.route('/view/mastodon/<string:topic>', methods=['GET'])
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


@app.route('/view/lang/<string:db>', methods=['GET'])
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


@app.route('/count/<string:db>', methods=['GET'])
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


if __name__ == '__main__':
    app.run(debug=True, port=8001)
