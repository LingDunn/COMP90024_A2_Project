import re
import os
import time
import json
import ijson
from mpi4py import MPI
from decimal import Decimal


file_path = '../data/twitter-huge.json'
save_path = 'data-geo/twitter-geo'
save_suffix = '.json'
tweet_head = b'^{"id":"\d+","key":'
pad_start = b'[\n'
pad_end = b'\n]\n'
batch_limit = 1024 * 1024


# Find the start of next twitter item from current file pointer
def find_tweet_start(fp, start):
    line = fp.readline()
    if not re.match(tweet_head, line):
        start += len(line)
    return start


def find_tweet_end(fp, end):
    next_line = fp.readline()
    if not re.match(tweet_head, next_line):
        end += (len(next_line[:-2]) - 1)
        if next_line == b'\n':
            end -= 1
    else:
        end -= 3
    return end


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
    else:
        end -= 4
    return start, end


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


def load_tweets(path, size, rank):
    file_size = os.path.getsize(path)
    chunk_size = file_size // size
    start = rank * chunk_size
    end = start + chunk_size if rank != size - 1 else file_size

    with open(path, 'rb+') as file:
        start, end = fix_batch_start_end(file, start, end, rank, size)
        file.seek(start)
        batch_size = end - start

        with open(f"{save_path}{rank}{save_suffix}", 'wb') as f:
            f.write(b'[')

            if batch_size > batch_limit:
                num_batch = (batch_size // batch_limit) + 1

                for i in range(num_batch):
                    tmp_start = start + i * batch_limit
                    tmp_end = tmp_start + batch_limit if i != num_batch - 1 else end
                    tmp_start, tmp_end = fix_piece_start_end(file, tmp_start, tmp_end, i, num_batch - 1)

                    file.seek(tmp_start)
                    json_raw = pad_start + file.read(tmp_end - tmp_start) + pad_end
                    items = ijson.items(json_raw, 'item')

                    for item in items:
                        if 'includes' in item['doc'].keys():
                            item_str = json.dumps(item, cls=JSONEncoder, ensure_ascii=False).encode('utf-8')
                            item_str += b','
                            f.write(item_str)

            else:
                json_raw = pad_start + file.read(end - start) + pad_end
                items = ijson.items(json_raw, 'item')
                f.write(b'[')
                for item in items:
                    if 'includes' in item['doc'].keys():
                        item_str = json.dumps(item, cls=JSONEncoder, ensure_ascii=False).encode('utf-8')
                        item_str += b','
                        f.write(item_str)

    with open(f"{save_path}{rank}{save_suffix}", 'rb') as f:
        contents = f.read()
    contents = contents[:-1] + b']'

    with open(f"{save_path}{rank}{save_suffix}", 'wb') as f:
        f.write(contents)


def process():
    start_time = time.time()
    # MPI settings
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    load_tweets(file_path, size, rank)
    comm.Barrier()

    if rank == 0:
        return start_time
    return None


if __name__ == '__main__':
    raw = process()
    if raw is not None:
        print(f"Time: {(time.time() - raw):.2f}s")
