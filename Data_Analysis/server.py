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


from flask import Flask, request, jsonify
from flask_cors import CORS
from api import conn, get_db, view_sum
from api import twt_topic_dist
from api import mas_topic_view
from api import lang_view
from api import twt_topic_count
from api import get_hashtags_cnt
from api import twt_state_topic_dist
from api import get_sudo_avg
from api import twt_state_topic_view
import copy
import string

app = Flask(__name__)
cors = CORS(app)


#################
#   DASHBOARD   #
#################
@app.route("/dashboard_lang_mas")
def dashboard_lang_mas():
    """
    Return data for Dashboard IV: mastodon language distribution pie, top 8.
    """
    lan_li = lang_view("mastodon")
    to_sort = []
    for item in lan_li:
        try:
            ele = [item["key"], item["value"]]
        except:
            pass
        to_sort.append(copy.deepcopy(ele))
    to_sort.sort(key=lambda x: x[1], reverse=True)
    # construct result
    data = {"lang": [], "value": []}
    lang = []
    value = []
    other = 0
    for i in range(len(to_sort)):
        if i < 8:
            lang.append(to_sort[i][0])
            value.append(to_sort[i][1])
        else:
            other += to_sort[i][1]
    try:
        lang.append("others")
        value.append(other)
    except:
        pass
    data["lang"] = copy.deepcopy(lang)
    data["value"] = copy.deepcopy(value)

    return data


@app.route("/dashboard_lang_twt")
def dashboard_lang_twt():
    """
    Return data for Dashboard IV: Twitter language distribution pie, top 8.
    """
    lan_li = lang_view("twitter")
    to_sort = []
    for item in lan_li:
        try:
            ele = [item["key"], item["value"]]
        except:
            pass
        to_sort.append(copy.deepcopy(ele))
    to_sort.sort(key=lambda x: x[1], reverse=True)
    # construct result
    data = {"lang": [], "value": []}
    lang = []
    value = []
    other = 0
    for i in range(len(to_sort)):
        if i < 8:
            lang.append(to_sort[i][0])
            value.append(to_sort[i][1])
        else:
            other += to_sort[i][1]
    lang.append("others")
    value.append(other)
    data["lang"] = copy.deepcopy(lang)
    data["value"] = copy.deepcopy(value)

    return data


@app.route("/sum_mas")
def sum_mas():
    """
    Return data for Dashboard IV: return number of docs in mastodon data, using db.info()
    """
    try:
        couch = conn()
        db = get_db(couch, 'mastodon_processed')
        data = {}
        data["sum_mas"] = db.info()["doc_count"]
        return data
    except:
        return {"error": "Unable to connect to database"}


@app.route("/sum_twt")
def sum_twt():
    """
    Return data for Dashboard IV: return number of docs in twitter data, using db.info()
    """
    try:
        couch = conn()
        db = get_db(couch, 'twitter-geo')
        data = {}
        data["sum_twt"] = db.info()['doc_count']
        return data
    except:
        return {"error": "Unable to connect to database"}


@app.route("/sum_sudo")
def sum_sudo():
    """
    Return data for Dashboard IV: return number of docs for sudo data, using db.info()
    """
    try:
        data = {}
        count = 0

        couch = conn()
        db = get_db(couch, 'sudo_gi')
        count += int(db.info()['doc_count'])
        db = get_db(couch, 'sudo_avg')
        count += int(db.info()['doc_count'])
        db = get_db(couch, 'state_suburb')
        count += int(db.info()['doc_count'])

        data["sum_sudo"] = count
        return data
    except:
        return {"error": "Unable to connect to database"}


@app.route("/dashboard_sudo_pie")
def dashboard_sudo_pie():
    """
    Return data for Dashboard IV: SUDO suburb per sata pie.
    """
    try:
        couch = conn()
        db = get_db(couch, 'state_suburb')
        mquery = {'selector': {},
                  'fields': ["state", "suburbs"],
                  "execution_stats": True}
        res = db.find(mquery)

        data = {"states": [], "suburbs": {}}
        for v in res:
            data["states"].append(v["state"])
            data["suburbs"][v["state"]] = v["suburbs"]
        return data
    except:
        return {"error": "Unable to connect to database"}


@app.route("/dashboard_topic_twt")
def dashboard_topic_twt():
    """
    Return data for Dashboard IV: Twitter Topic Radar.
    """
    res = twt_topic_count()
    topic = res["topics"]
    cnts = res["cnts"]
    dict = {}
    for i in range(len(topic)):
        dict[topic[i]] = cnts[i]
    data = {"counts": [dict["scotty"], dict["ukraine"], dict["cc"], dict["nft"], dict["porn"]]}

    return data


@app.route("/dashboard_topic_mas")
def dashboard_topic_mas():
    """
    Return data for Dashboard IV: Mas topic Radar.
    """
    # try:
    m_c = mas_topic_view("scotty")["scotty"]
    u_c = mas_topic_view("ukraine")["ukraine"]
    c_c = mas_topic_view("cc")["cc"]
    n_c = mas_topic_view("nft")["nft"]
    p_c = mas_topic_view("porn")["porn"]
    data = {"counts": [m_c, u_c, c_c, n_c, p_c]}
    return data
    # except:
    # return {"error": "Unable to connect to database"}


@app.route("/dashboard_hashtag")
def dashboard_hashtag():
    """
    Dashboard IV: Twitter hashtag top8.
    """
    data = get_hashtags_cnt(8)
    return data


##############
#   SCOTTY   #
##############
@app.route("/sm_twt_pie")
def sm_twt_pie():
    """
    SM topic IV: Twitter Count pie.
    """
    # try:
    res = twt_topic_count()
    topic = res["topics"]
    cnts = res["cnts"]
    dict = {}
    for i in range(len(topic)):
        dict[topic[i]] = cnts[i]
    m_c = dict["scotty"]
    rest = dict["ukraine"] + dict["cc"] + dict["nft"] + dict["porn"]
    data = {"counts": [m_c, rest]}
    return data
    # except:
    # return {"error": "Unable to connect to database"}


@app.route("/sm_mas_pie")
def sm_mas_pie():
    """
    SM topic IV: Mastodon count pie
    """
    # try:
    m_c = mas_topic_view("scotty")["scotty"]
    rest = m_c
    rest += mas_topic_view("ukraine")["ukraine"]
    rest += mas_topic_view("cc")["cc"]
    rest += mas_topic_view("nft")["nft"]
    rest += mas_topic_view("porn")["porn"]
    data = {"counts": [m_c, rest]}
    return data
    # except:
    # return {"error": "Unable to connect to database"}


@app.route("/sm_map_data")
def sm_map_data():
    """
    SM Map + Dist: all data retrived at once.
    """
    states = ['new south wales',
              'victoria',
              'queensland',
              'south australia',
              'western australia',
              'tasmania',
              'northern territory',
              'australian capital territory']
    final_res = {}

    # prepare map
    res = []
    state_dist_dic = {}
    for state in states:
        tmp = {}
        tmp["state"] = string.capwords(state)
        tmp_avg = get_sudo_avg(state)
        tmp["mid_age"] = tmp_avg["med_age"]
        tmp["mid_week_inc"] = tmp_avg["med_week_inc"]

        state_dist_dic[state] = copy.deepcopy(twt_state_topic_dist("scotty", state))
        tmp["cnt"] = state_dist_dic[state]["count"]
        tmp["sent"] = round(state_dist_dic[state]["avg_sent"], 3)
        res.append(copy.deepcopy(tmp))

    final_res["map_data"] = copy.deepcopy(res)

    # prepare dist
    # AUS
    final_res["aus"] = twt_topic_dist("scotty")
    final_res["aus"]["sub"] = ", ".join([string.capwords(state) for state in states])
    # NSW
    final_res["nsw"] = state_dist_dic["new south wales"]
    final_res["nsw"]["sub"] = get_suburb(twt_state_topic_view("scotty", "new south wales"))
    # VIC
    final_res["vic"] = state_dist_dic["victoria"]
    final_res["vic"]["sub"] = get_suburb(twt_state_topic_view("scotty", "victoria"))
    # QSL
    final_res["qsl"] = state_dist_dic["queensland"]
    final_res["qsl"]["sub"] = get_suburb(twt_state_topic_view("scotty", "queensland"))
    # WA
    final_res["wa"] = state_dist_dic["western australia"]
    final_res["wa"]["sub"] = get_suburb(twt_state_topic_view("scotty", "western australia"))
    # SA
    final_res["sa"] = state_dist_dic["south australia"]
    final_res["sa"]["sub"] = get_suburb(twt_state_topic_view("scotty", "south australia"))
    # TAS
    final_res["tas"] = state_dist_dic["tasmania"]
    final_res["tas"]["sub"] = get_suburb(twt_state_topic_view("scotty", "tasmania"))
    # NT
    final_res["nt"] = state_dist_dic["northern territory"]
    final_res["nt"]["sub"] = get_suburb(twt_state_topic_view("scotty", "northern territory"))
    # ACT
    final_res["act"] = state_dist_dic["australian capital territory"]
    final_res["act"]["sub"] = get_suburb(twt_state_topic_view("scotty", "australian capital territory"))

    return final_res


##############
#   UKRAINE  #
##############
@app.route("/uk_twt_pie")
def uk_twt_pie():
    """
    UK topic IV: Twitter Count pie.
    """
    # try:
    res = twt_topic_count()
    topic = res["topics"]
    cnts = res["cnts"]
    dict = {}
    for i in range(len(topic)):
        dict[topic[i]] = cnts[i]
    m_c = dict["ukraine"]
    rest = dict["scotty"] + dict["cc"] + dict["nft"] + dict["porn"]
    data = {"counts": [m_c, rest]}
    return data
    # except:
    # return {"error": "Unable to connect to database"}


@app.route("/uk_mas_pie")
def uk_mas_pie():
    """
    UK topic IV: Mastodon count pie
    """
    # try:
    m_c = mas_topic_view("ukraine")["ukraine"]
    rest = m_c
    rest += mas_topic_view("scotty")["scotty"]
    rest += mas_topic_view("cc")["cc"]
    rest += mas_topic_view("nft")["nft"]
    rest += mas_topic_view("porn")["porn"]
    data = {"counts": [m_c, rest]}
    return data
    # except:
    # return {"error": "Unable to connect to database"}


@app.route("/uk_map_data")
def uk_map_data():
    """
    UK Map + Dist: all data retrived at once.
    """
    topic = "ukraine"
    states = ['new south wales',
              'victoria',
              'queensland',
              'south australia',
              'western australia',
              'tasmania',
              'northern territory',
              'australian capital territory']
    final_res = {}

    # prepare map
    res = []
    state_dist_dic = {}
    for state in states:
        tmp = {}
        tmp["state"] = string.capwords(state)
        tmp_avg = get_sudo_avg(state)
        tmp["mid_age"] = tmp_avg["med_age"]
        tmp["mid_week_inc"] = tmp_avg["med_week_inc"]
        state_dist_dic[state] = copy.deepcopy(twt_state_topic_dist(topic, state))
        tmp["cnt"] = state_dist_dic[state]["count"]
        tmp["sent"] = round(state_dist_dic[state]["avg_sent"], 3)
        res.append(copy.deepcopy(tmp))
    final_res["map_data"] = copy.deepcopy(res)

    # prepare dist
    # AUS
    final_res["aus"] = twt_topic_dist(topic)
    final_res["aus"]["sub"] = ", ".join([string.capwords(state) for state in states])
    # NSW
    final_res["nsw"] = state_dist_dic["new south wales"]
    final_res["nsw"]["sub"] = get_suburb(twt_state_topic_view(topic, "new south wales"))
    # VIC
    final_res["vic"] = state_dist_dic["victoria"]
    final_res["vic"]["sub"] = get_suburb(twt_state_topic_view(topic, "victoria"))
    # QSL
    final_res["qsl"] = state_dist_dic["queensland"]
    final_res["qsl"]["sub"] = get_suburb(twt_state_topic_view(topic, "queensland"))
    # WA
    final_res["wa"] = state_dist_dic["western australia"]
    final_res["wa"]["sub"] = get_suburb(twt_state_topic_view(topic, "western australia"))
    # SA
    final_res["sa"] = state_dist_dic["south australia"]
    final_res["sa"]["sub"] = get_suburb(twt_state_topic_view(topic, "south australia"))
    # TAS
    final_res["tas"] = state_dist_dic["tasmania"]
    final_res["tas"]["sub"] = get_suburb(twt_state_topic_view(topic, "tasmania"))
    # NT
    final_res["nt"] = state_dist_dic["northern territory"]
    final_res["nt"]["sub"] = get_suburb(twt_state_topic_view(topic, "northern territory"))
    # ACT
    final_res["act"] = state_dist_dic["australian capital territory"]
    final_res["act"]["sub"] = get_suburb(twt_state_topic_view(topic, "australian capital territory"))

    return final_res


##############
#   CRYPTO   #
##############
@app.route("/cc_twt_pie")
def cc_twt_pie():
    """
    CC topic IV: Twitter Count pie.
    """
    # try:
    res = twt_topic_count()
    topic = res["topics"]
    cnts = res["cnts"]
    dict = {}
    for i in range(len(topic)):
        dict[topic[i]] = cnts[i]
    m_c = dict["cc"]
    rest = dict["scotty"] + dict["ukraine"] + dict["nft"] + dict["porn"]
    data = {"counts": [m_c, rest]}
    return data
    # except:
    # return {"error": "Unable to connect to database"}


@app.route("/cc_mas_pie")
def cc_mas_pie():
    """
    CC topic IV: Mastodon count pie
    """
    # try:
    m_c = mas_topic_view("cc")["cc"]
    rest = m_c
    rest += mas_topic_view("scotty")["scotty"]
    rest += mas_topic_view("ukraine")["ukraine"]
    rest += mas_topic_view("nft")["nft"]
    rest += mas_topic_view("porn")["porn"]
    data = {"counts": [m_c, rest]}
    return data
    # except:
    # return {"error": "Unable to connect to database"}


@app.route("/cc_map_data")
def cc_map_data():
    """
    CC Map + Dist: all data retrived at once.
    """
    topic = "cc"
    states = ['new south wales',
              'victoria',
              'queensland',
              'south australia',
              'western australia',
              'tasmania',
              'northern territory',
              'australian capital territory']
    final_res = {}

    # prepare map
    res = []
    state_dist_dic = {}
    for state in states:
        tmp = {}
        tmp["state"] = string.capwords(state)
        tmp_avg = get_sudo_avg(state)
        tmp["mid_age"] = tmp_avg["med_age"]
        tmp["mid_week_inc"] = tmp_avg["med_week_inc"]
        state_dist_dic[state] = copy.deepcopy(twt_state_topic_dist(topic, state))
        tmp["cnt"] = state_dist_dic[state]["count"]
        tmp["sent"] = round(state_dist_dic[state]["avg_sent"], 3)
        res.append(copy.deepcopy(tmp))
    final_res["map_data"] = copy.deepcopy(res)

    # prepare dist
    # AUS
    final_res["aus"] = twt_topic_dist(topic)
    final_res["aus"]["sub"] = ", ".join([string.capwords(state) for state in states])
    # NSW
    final_res["nsw"] = state_dist_dic["new south wales"]
    final_res["nsw"]["sub"] = get_suburb(twt_state_topic_view(topic, "new south wales"))
    # VIC
    final_res["vic"] = state_dist_dic["victoria"]
    final_res["vic"]["sub"] = get_suburb(twt_state_topic_view(topic, "victoria"))
    # QSL
    final_res["qsl"] = state_dist_dic["queensland"]
    final_res["qsl"]["sub"] = get_suburb(twt_state_topic_view(topic, "queensland"))
    # WA
    final_res["wa"] = state_dist_dic["western australia"]
    final_res["wa"]["sub"] = get_suburb(twt_state_topic_view(topic, "western australia"))
    # SA
    final_res["sa"] = state_dist_dic["south australia"]
    final_res["sa"]["sub"] = get_suburb(twt_state_topic_view(topic, "south australia"))
    # TAS
    final_res["tas"] = state_dist_dic["tasmania"]
    final_res["tas"]["sub"] = get_suburb(twt_state_topic_view(topic, "tasmania"))
    # NT
    final_res["nt"] = state_dist_dic["northern territory"]
    final_res["nt"]["sub"] = get_suburb(twt_state_topic_view(topic, "northern territory"))
    # ACT
    final_res["act"] = state_dist_dic["australian capital territory"]
    final_res["act"]["sub"] = get_suburb(twt_state_topic_view(topic, "australian capital territory"))

    return final_res


###########
#   NFT   #
###########
@app.route("/nft_twt_pie")
def nft_twt_pie():
    """
    NFT topic IV: Twitter Count pie.
    """
    # try:
    res = twt_topic_count()
    topic = res["topics"]
    cnts = res["cnts"]
    dict = {}
    for i in range(len(topic)):
        dict[topic[i]] = cnts[i]
    m_c = dict["nft"]
    rest = dict["scotty"] + dict["ukraine"] + dict["cc"] + dict["porn"]
    data = {"counts": [m_c, rest]}
    return data
    # except:
    # return {"error": "Unable to connect to database"}


@app.route("/nft_mas_pie")
def nft_mas_pie():
    """
    NFT topic IV: Mastodon count pie
    """
    # try:
    m_c = mas_topic_view("nft")["nft"]
    rest = m_c
    rest += mas_topic_view("scotty")["scotty"]
    rest += mas_topic_view("ukraine")["ukraine"]
    rest += mas_topic_view("cc")["cc"]
    rest += mas_topic_view("porn")["porn"]
    data = {"counts": [m_c, rest]}
    return data
    # except:
    # return {"error": "Unable to connect to database"}


@app.route("/nft_map_data")
def nft_map_data():
    """
    NFT Map + Dist: all data retrived at once.
    """
    topic = "nft"
    states = ['new south wales',
              'victoria',
              'queensland',
              'south australia',
              'western australia',
              'tasmania',
              'northern territory',
              'australian capital territory']
    final_res = {}

    # prepare map
    res = []
    state_dist_dic = {}
    for state in states:
        tmp = {}
        tmp["state"] = string.capwords(state)
        tmp_avg = get_sudo_avg(state)
        tmp["mid_age"] = tmp_avg["med_age"]
        tmp["mid_week_inc"] = tmp_avg["med_week_inc"]
        state_dist_dic[state] = copy.deepcopy(twt_state_topic_dist(topic, state))
        tmp["cnt"] = state_dist_dic[state]["count"]
        tmp["sent"] = round(state_dist_dic[state]["avg_sent"], 3)
        res.append(copy.deepcopy(tmp))
    final_res["map_data"] = copy.deepcopy(res)

    # prepare dist
    # AUS
    final_res["aus"] = twt_topic_dist(topic)
    final_res["aus"]["sub"] = ", ".join([string.capwords(state) for state in states])
    # NSW
    final_res["nsw"] = state_dist_dic["new south wales"]
    final_res["nsw"]["sub"] = get_suburb(twt_state_topic_view(topic, "new south wales"))
    # VIC
    final_res["vic"] = state_dist_dic["victoria"]
    final_res["vic"]["sub"] = get_suburb(twt_state_topic_view(topic, "victoria"))
    # QSL
    final_res["qsl"] = state_dist_dic["queensland"]
    final_res["qsl"]["sub"] = get_suburb(twt_state_topic_view(topic, "queensland"))
    # WA
    final_res["wa"] = state_dist_dic["western australia"]
    final_res["wa"]["sub"] = get_suburb(twt_state_topic_view(topic, "western australia"))
    # SA
    final_res["sa"] = state_dist_dic["south australia"]
    final_res["sa"]["sub"] = get_suburb(twt_state_topic_view(topic, "south australia"))
    # TAS
    final_res["tas"] = state_dist_dic["tasmania"]
    final_res["tas"]["sub"] = get_suburb(twt_state_topic_view(topic, "tasmania"))
    # NT
    final_res["nt"] = state_dist_dic["northern territory"]
    final_res["nt"]["sub"] = get_suburb(twt_state_topic_view(topic, "northern territory"))
    # ACT
    final_res["act"] = state_dist_dic["australian capital territory"]
    final_res["act"]["sub"] = get_suburb(twt_state_topic_view(topic, "australian capital territory"))

    return final_res


############
#   PORN   #
############
@app.route("/porn_twt_pie")
def porn_twt_pie():
    """
    PORN topic IV: Twitter Count pie.
    """
    # try:
    res = twt_topic_count()
    topic = res["topics"]
    cnts = res["cnts"]
    dict = {}
    for i in range(len(topic)):
        dict[topic[i]] = cnts[i]
    m_c = dict["porn"]
    rest = dict["scotty"] + dict["ukraine"] + dict["cc"] + dict["nft"]
    data = {"counts": [m_c, rest]}
    return data
    # except:
    # return {"error": "Unable to connect to database"}


@app.route("/porn_mas_pie")
def porn_mas_pie():
    """
    PORN topic IV: Mastodon count pie
    """
    # try:
    m_c = mas_topic_view("porn")["porn"]
    rest = m_c
    rest += mas_topic_view("scotty")["scotty"]
    rest += mas_topic_view("ukraine")["ukraine"]
    rest += mas_topic_view("nft")["nft"]
    rest += mas_topic_view("cc")["cc"]
    data = {"counts": [m_c, rest]}
    return data
    # except:
    # return {"error": "Unable to connect to database"}


@app.route("/porn_map_data")
def porn_map_data():
    """
    PORN Map + Dist: all data retrived at once.
    """
    topic = "porn"
    states = ['new south wales',
              'victoria',
              'queensland',
              'south australia',
              'western australia',
              'tasmania',
              'northern territory',
              'australian capital territory']
    final_res = {}

    # prepare map
    res = []
    state_dist_dic = {}
    for state in states:
        tmp = {}
        tmp["state"] = string.capwords(state)
        tmp_avg = get_sudo_avg(state)
        tmp["mid_age"] = tmp_avg["med_age"]
        tmp["mid_week_inc"] = tmp_avg["med_week_inc"]
        state_dist_dic[state] = copy.deepcopy(twt_state_topic_dist(topic, state))
        tmp["cnt"] = state_dist_dic[state]["count"]
        tmp["sent"] = round(state_dist_dic[state]["avg_sent"], 3)
        res.append(copy.deepcopy(tmp))
    final_res["map_data"] = copy.deepcopy(res)

    # prepare dist
    # AUS
    final_res["aus"] = twt_topic_dist(topic)
    final_res["aus"]["sub"] = ", ".join([string.capwords(state) for state in states])
    # NSW
    final_res["nsw"] = state_dist_dic["new south wales"]
    final_res["nsw"]["sub"] = get_suburb(twt_state_topic_view(topic, "new south wales"))
    # VIC
    final_res["vic"] = state_dist_dic["victoria"]
    final_res["vic"]["sub"] = get_suburb(twt_state_topic_view(topic, "victoria"))
    # QSL
    final_res["qsl"] = state_dist_dic["queensland"]
    final_res["qsl"]["sub"] = get_suburb(twt_state_topic_view(topic, "queensland"))
    # WA
    final_res["wa"] = state_dist_dic["western australia"]
    final_res["wa"]["sub"] = get_suburb(twt_state_topic_view(topic, "western australia"))
    # SA
    final_res["sa"] = state_dist_dic["south australia"]
    final_res["sa"]["sub"] = get_suburb(twt_state_topic_view(topic, "south australia"))
    # TAS
    final_res["tas"] = state_dist_dic["tasmania"]
    final_res["tas"]["sub"] = get_suburb(twt_state_topic_view(topic, "tasmania"))
    # NT
    final_res["nt"] = state_dist_dic["northern territory"]
    final_res["nt"]["sub"] = get_suburb(twt_state_topic_view(topic, "northern territory"))
    # ACT
    final_res["act"] = state_dist_dic["australian capital territory"]
    final_res["act"]["sub"] = get_suburb(twt_state_topic_view(topic, "australian capital territory"))

    return final_res


def get_suburb(data):
    """
    Getting the suburb name from given list of dic.
    """
    res = ""
    for item in data:
        res += string.capwords(item["suburb"]) + ", "
    return res


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
