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


from flask import Flask, request, json
from flask_cors import CORS
from api import conn, get_db, view_sum
from api import twt_topic_dist
from api import mas_topic_view
from api import lang_view
from api import twt_topic_count
from api import get_hashtags_cnt
from api import twt_state_topic_dist
from api import get_sudo_avg
from api import twt_state_topic_view, prepare_dist, get_topic_counts, get_mas_topic_counts


app = Flask(__name__)
cors = CORS(app)

scotty_map = json.dumps(prepare_dist("scotty"))
porn_map = json.dumps(prepare_dist("porn"))
cc_map = json.dumps(prepare_dist("cc"))
uk_map = json.dumps(prepare_dist("ukraine"))
nft_map = json.dumps(prepare_dist("nft"))

#################
#   DASHBOARD   #
#################
@app.route("/")
def hello():
    return "Hello"


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
        to_sort.append(ele)
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
    data["lang"] = lang
    data["value"] = value

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
        to_sort.append(ele)
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
    data["lang"] = lang
    data["value"] = value

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
    return get_mas_topic_counts("scotty")


@app.route("/sm_map_data")
def sm_map_data():
    """
    SM Map + Dist: all data retrived at once.
    """
    return scotty_map


##############
#   UKRAINE  #
##############
@app.route("/uk_twt_pie")
def uk_twt_pie():
    """
    UK topic IV: Twitter Count pie.
    """
    return get_topic_counts("ukraine")


@app.route("/uk_mas_pie")
def uk_mas_pie():
    """
    UK topic IV: Mastodon count pie
    """
    return get_mas_topic_counts("ukraine")


@app.route("/uk_map_data")
def uk_map_data():
    """
    UK Map + Dist: all data retrived at once.
    """
    return uk_map


##############
#   CRYPTO   #
##############
@app.route("/cc_twt_pie")
def cc_twt_pie():
    """
    CC topic IV: Twitter Count pie.
    """
    return get_topic_counts("cc")


@app.route("/cc_mas_pie")
def cc_mas_pie():
    """
    CC topic IV: Mastodon count pie
    """
    return get_mas_topic_counts("cc")


@app.route("/cc_map_data")
def cc_map_data():
    """
    CC Map + Dist: all data retrived at once.
    """
    return cc_map


###########
#   NFT   #
###########
@app.route("/nft_twt_pie")
def nft_twt_pie():
    """
    NFT topic IV: Twitter Count pie.
    """
    return get_topic_counts("nft")


@app.route("/nft_mas_pie")
def nft_mas_pie():
    """
    NFT topic IV: Mastodon count pie
    """
    return get_mas_topic_counts("nft")


@app.route("/nft_map_data")
def nft_map_data():
    """
    NFT Map + Dist: all data retrived at once.
    """
    return nft_map


############
#   PORN   #
############
@app.route("/porn_twt_pie")
def porn_twt_pie():
    """
    PORN topic IV: Twitter Count pie.
    """
    return get_topic_counts("porn")


@app.route("/porn_mas_pie")
def porn_mas_pie():
    """
    PORN topic IV: Mastodon count pie
    """
    return get_mas_topic_counts("porn")


@app.route("/porn_map_data")
def porn_map_data():
    """
    PORN Map + Dist: all data retrived at once.
    """
    return porn_map

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    #app.run(port=5000, debug=True)