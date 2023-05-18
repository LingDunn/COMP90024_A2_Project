import json,csv
import requests, nltk, string
from bs4 import BeautifulSoup
import os, time
nltk.download('punkt')

# request on current data
websites=["https://aus.social/api/v1/timelines/public",
          "https://theblower.au/api/v1/timelines/public",
          "https://mastodon.au/api/v1/timelines/public"]

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
        params = {'local':True, 'min_id':max_id, 'limit':limit}
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

topics = ['web3', 'politics', 'porn']
sub_topics = ['cc', 'nft', 'scotty', 'ukraine']
def topic_cls(text, corpus1, corpus2):
    topic = []
    sub_topic = []
    for i, corpus in enumerate(corpus1):
        for word in corpus:
            if word in text:
                topic.append(topics[i])
                for j, sub_corpus in enumerate(corpus2):
                    for sub_word in sub_corpus:
                        if sub_word in text and sub_topics[j] not in sub_topic:
                            sub_topic.append(sub_topics[j])
                            break
                break
    return topic, sub_topic

def WordsExtractor(text):
    text = text.replace("*", " ")
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text()
    text=text.lower()
    text = ''.join(char for char in text if char not in string.punctuation)
    words = nltk.word_tokenize(text)
    return '|'.join(w for w in words)

def load_corpus(paths):
    corpus_list = []
    for path in paths:
        with open(path, 'r', encoding='utf-8') as fp:
            corpus_list.append([w.lower() for w in next(csv.reader(fp))])
    return corpus_list


corpus_cc_path = 'corpus/web3/cryptocurrency.csv'
corpus_nft_path = 'corpus/web3/nft.csv'
corpus_scotty_path = 'corpus/politics/scotty.csv'
corpus_ukraine_path = 'corpus/politics/ukraine.csv'
corpus_web3_path = 'corpus/web3.csv'
corpus_politics_path = 'corpus/politics.csv'
corpus_porn_path = 'corpus/porn.csv'
corpus_paths = [corpus_web3_path,
                corpus_politics_path,
                corpus_porn_path]
sub_corpus_paths = [corpus_cc_path,
                    corpus_nft_path,
                    corpus_scotty_path,
                    corpus_ukraine_path]
corpus_l1 = load_corpus(corpus_paths)
corpus_l2 = load_corpus(sub_corpus_paths)

def insert_data(db_name, _id, data):
    param = {'new_edits':True}
    url = couchDB_address + db_name+ '/' + _id
    resp = requests.put(url=url, data=data, params=param)
    if resp.status_code == 201:
        pass
    else:
        print(resp.text)

couchDB_address = 'http://admin:admin@172.26.135.87:5984/'
db_name = 'mastodon_processed'


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
            print("",websites[x],data[-1]["created_at"], "num tweets:",len(data))
            for tweets in data:
                newData = {}
                _id = tweets['id']
                newData['token'] = WordsExtractor(tweets['content'])
                newData['create_at'] = tweets["created_at"]
                newData['lang'] = tweets["language"]
                newData['text'] = tweets['content']
                if newData['token'] == "":
                    continue
                newData['sentiment'] = ''
                newData['suburb'] = ''
                newData['state'] = ''
                newData['tag'] = tweets['tags']
                newData['topic'], newData['sub_topic'] = topic_cls(newData['token'], corpus_l1, corpus_l2)
                insert_data(db_name, _id, json.dumps(newData))
        #store current last id in disk
        last_id_file = open("latest_id.txt", "w")
        for id in last_ids:
            last_id_file.writelines(id+'\n')
        last_id_file.close()

if __name__ == '__main__':
    update_data()