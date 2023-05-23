import os
import re
import csv
import json
import ijson
from mpi4py import MPI
from collections import Counter


data_path = '../data/twitter-geo.json'
tweet_head = b'{"tokens"'
pad_start = b'['
pad_end = b']'
hashtag_pattern = r"#\w*[^\x00-\x7F]*\w*"
batch_limit = 1024 * 1024


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
        end += len(next_line[:-2])
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


def get_hashtags(items):
    res = Counter()
    for item in items:
        text = item['text']
        ht = re.findall(hashtag_pattern, text, re.UNICODE)
        for h in ht:
            res[h.lower()] += 1
    return res


def load_analyze(file_path, size, rank):
    file_size = os.path.getsize(file_path)
    chunk_size = file_size // size
    start = rank * chunk_size
    end = start + chunk_size if rank != size - 1 else file_size

    hashtags = Counter()
    with open(file_path, 'rb') as fp:
        start, end = fix_batch_start_end(fp, start, end, rank, size)
        fp.seek(start)
        batch_size = end - start

        if batch_size > batch_limit:
            num_piece = (batch_size // batch_limit) + 1

            for i in range(num_piece):
                tmp_start = start + i * batch_limit
                tmp_end = tmp_start + batch_limit if i != num_piece - 1 else end
                tmp_start, tmp_end = fix_piece_start_end(fp, tmp_start, tmp_end, i, num_piece - 1)

                fp.seek(tmp_start)
                json_raw = (pad_start + fp.read(tmp_end - tmp_start) + pad_end).decode('utf-8')
                items = ijson.items(json_raw, 'item')
                hashtags.update(get_hashtags(items))

        else:
            json_raw = (pad_start + fp.read(end - start) + pad_end).decode('utf-8')
            items = ijson.items(json_raw, 'item')
            hashtags.update(get_hashtags(items))

    return hashtags


def process():
    # MPI settings
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    batch = load_analyze(data_path, size, rank)
    comm.Barrier()
    items_list = comm.gather(batch, root=0)

    if rank == 0:
        results = [item for item in items_list]
        return results


raw = process()

if raw is not None:
    merged_counter = Counter()
    for cnt in raw:
        merged_counter.update(cnt)

    # with open('../hashtag/hashtags.csv', 'w', newline='', encoding='utf-8') as output_file:
    #     writer = csv.writer(output_file)
    #     writer.writerow(list(merged_counter.keys()))

    # hashtag_data = json.dumps(merged_counter.most_common(), ensure_ascii=False).encode('utf-8')
    # # Write the string representation to a file using UTF-8 encoding
    # with open("../hashtag/hashtags-cnt.json", "wb") as f:
    #     f.write(hashtag_data)

    # formatted_data = [{"hashtag": key, "cnt": value} for key, value in merged_counter.items()]
    # with open("../hashtag/hashtags_cnt.json", "w") as json_file:
    #     json.dump(formatted_data, json_file)
