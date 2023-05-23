import json
import ijson
import requests
from tqdm import tqdm
from decimal import Decimal


db_addr = 'http://admin:admin@172.26.135.87:5984/'
suffix = '_bulk_docs'


pad_start_b = b'['
pad_end_b = b']'
pad_start = '['
pad_end = ']'


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def create_db(db_name):
    url = db_addr + db_name
    resp = requests.put(url=url)
    print(resp.text)


def insert_batch_bulk(data_path, db_name, num_data):
    batch_size = 500
    param = {'new_edits': True}
    pbar = tqdm(total=num_data, dynamic_ncols=True)
    with open(data_path, 'rb') as f:
        items = ijson.items(f, 'item')
        i = 1
        data = b'['
        for item in items:
            row = json.dumps(item, cls=JSONEncoder, ensure_ascii=False).encode("utf-8")
            data += row + b',\n'
            if i % batch_size == 0 or i == num_data:
                data = json.loads(b'{"docs": ' + data[:-2] + b']}')
                response = requests.post(db_addr + db_name + '/' + suffix, json=data, params=param)
                if response.status_code != 201:
                    print("Error uploading data: ", response.json())
                data = b'['
            i += 1
            pbar.update()
    pbar.close()
    print("Data uploaded successfully.")


def insert_bulk(data_path, db_name, pad=True):
    param = {'new_edits': True}
    with open(data_path, 'r', encoding='utf-8') as f:
        data = pad_start + f.read() + pad_end if pad else f.read()
        data = json.loads(data)
        # data = json.dumps(data, cls=JSONEncoder)
        response = requests.post(db_addr + db_name + '/' + suffix, json={"docs": data}, params=param)

        # Check the status code of the response
        if response.status_code == 201:
            print("Data uploaded successfully.")
        else:
            print("Error uploading data: ", response.json())


database = 'sudo_avg'
file_path = '../sudo/state-avg.json'

# create_db(database)
# insert_batch_bulk(file_path, database, 175165)
# insert_bulk(file_path, database)
# insert_bulk(file_path, database, False)
