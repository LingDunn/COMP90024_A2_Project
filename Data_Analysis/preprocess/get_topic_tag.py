import os
import re
import csv
import time
import json
import ijson
from mpi4py import MPI
from decimal import Decimal

topics = ['web3', 'politics', 'porn']
sub_topics = ['cc', 'nft', 'scotty', 'ukraine']

corpus_web3_path = '../corpus/web3.csv'
corpus_politics_path = '../corpus/politics.csv'
corpus_porn_path = '../corpus/porn.csv'
corpus_paths = [corpus_web3_path,
                corpus_politics_path,
                corpus_porn_path]

corpus_cc_path = '../corpus/web3/cryptocurrency.csv'
corpus_nft_path = '../corpus/web3/nft.csv'
corpus_scotty_path = '../corpus/politics/scotty.csv'
corpus_ukraine_path = '../corpus/politics/ukraine.csv'
sub_corpus_paths = [corpus_cc_path,
                    corpus_nft_path,
                    corpus_scotty_path,
                    corpus_ukraine_path]

tag_web3_path = '../hashtag/web3.csv'
tag_politics_path = '../hashtag/politics.csv'
tag_porn_path = '../hashtag/porn.csv'
tag_paths = [tag_web3_path,
             tag_politics_path,
             tag_porn_path]

tag_cc_path = '../hashtag/web3/cryptocurrency.csv'
tag_nft_path = '../hashtag/web3/nft.csv'
tag_scotty_path = '../hashtag/politics/scotty.csv'
tag_ukraine_path = '../hashtag/politics/ukraine.csv'
sub_tag_paths = [tag_cc_path,
                 tag_nft_path,
                 tag_scotty_path,
                 tag_ukraine_path]

hashtag_pattern = r"#\w*[^\x00-\x7F]*\w*"
data_path = "../data/twitter-geo.json"
tweet_head = b'{"tokens"'
pad_start = b'['
pad_end = b']'
save_path = "../data/twitter-topic.json"
batch_limit = 1024 * 1024


def load_corpus(paths):
    corpus_list = []
    for path in paths:
        with open(path, 'r', encoding='utf-8') as fp:
            corpus_list.append([w.lower() for w in next(csv.reader(fp))])
    return corpus_list


# Find the start of next twitter item from current file pointer
def find_tweet_start(fp, start):
    line = fp.readline()
    if not re.match(tweet_head, line):
        start += len(line)
    return start


# Find the end of current twitter item from current file pointer
def find_tweet_end(fp, end):
    next_line = fp.readline()
    if not re.match(tweet_head, next_line):
        end += (len(next_line[:-2]))
        if next_line == b'\n':
            end -= 1
    else:
        end -= 2
    return end


# Modify the start and end pointers of the batch to ensure twitter items are complete
def fix_batch_start_end(fp, start, end, rank, size):
    fp.seek(start)
    if start == 0:
        line = fp.readline()
        start += len(line)
    else:
        start = find_tweet_start(fp, start)

    if rank < size - 1:
        fp.seek(end)
        end = find_tweet_end(fp, end)
    return start, end


# Modify the start and end pointers of the piece to ensure twitter items are complete
def fix_piece_start_end(fp, start, end, index, tail):
    if index != 0:
        fp.seek(start)
        start = find_tweet_start(fp, start)

    if index != tail:
        fp.seek(end)
        end = find_tweet_end(fp, end)

    return start, end


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


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


# Analyze each tweet and update stats
def get_topic_tag(tweets, corpus1, corpus2):
    res = b''
    for tweet in tweets:
        tweet_text = tweet['text'].lower()
        tweet_tag = [t.lower() for t in re.findall(hashtag_pattern, tweet_text, re.UNICODE)]
        tweet_topic, tweet_sub_topic = topic_cls(tweet_text, corpus1, corpus2)
        tweet['tag'] = tweet_tag
        tweet['topic'] = tweet_topic
        tweet['sub_topic'] = tweet_sub_topic
        tweet_data = json.dumps(tweet, cls=JSONEncoder, ensure_ascii=False).encode("utf-8")
        res += tweet_data + b',\n'
    return res


# Load, process and analyze twitter data
def load_tweets(file_path, size, rank, corpus1, corpus2):
    file_size = os.path.getsize(file_path)
    chunk_size = file_size // size

    start = rank * chunk_size
    end = start + chunk_size if rank != size - 1 else file_size

    res = b''
    with open(file_path, 'rb') as file:
        start, end = fix_batch_start_end(file, start, end, rank, size)
        file.seek(start)
        batch_size = end - start

        if batch_size > batch_limit:
            num_batch = (batch_size // batch_limit) + 1

            for i in range(num_batch):
                tmp_start = start + i * batch_limit
                tmp_end = tmp_start + batch_limit if i != num_batch - 1 else end
                tmp_start, tmp_end = fix_piece_start_end(file, tmp_start, tmp_end, i, num_batch - 1)

                file.seek(tmp_start)
                json_raw = pad_start + file.read(tmp_end - tmp_start) + pad_end
                items = ijson.items(json_raw, 'item')
                res += get_topic_tag(items, corpus1, corpus2)
        else:
            json_raw = pad_start + file.read(end - start) + pad_end
            items = ijson.items(json_raw, 'item')
            res += get_topic_tag(items, corpus1, corpus2)

    return res


# Encapsulate the whole process and return the stats
def process():
    start_time = time.time()
    # MPI settings
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # tag_corpus = load_corpus(tag_paths)
    # sub_tag_corpus = load_corpus(sub_tag_paths)
    corpus_l1 = load_corpus(corpus_paths)
    corpus_l2 = load_corpus(sub_corpus_paths)
    batch = load_tweets(data_path, size, rank, corpus_l1, corpus_l2)
    comm.Barrier()
    raw_data = comm.gather(batch, root=0)

    if rank == 0:
        res_list = [item for item in raw_data]
        return res_list, start_time
    return None


if __name__ == '__main__':
    raw = process()

    if raw is not None:
        data = b'['
        for part in raw[0]:
            data += part
        data = data[:-2] + b']'
        with open(save_path, "wb") as f:
            f.write(data)
        print(f"Time: {(time.time() - raw[1]):.2f}")
