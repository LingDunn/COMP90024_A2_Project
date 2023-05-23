import re
import json
import ijson
from tqdm import tqdm
from decimal import Decimal
from os import listdir
from os.path import isfile, join


states = ['new south wales',
          'victoria',
          'queensland',
          'south australia',
          'western australia',
          'tasmania',
          'northern territory',
          'australian capital territory'
          ]

capitals = {
    'sydney': 'new south wales',
    'melbourne': 'victoria',
    'brisbane': 'queensland',
    'adelaide': 'south australia',
    'perth': 'western australia',
    'hobart': 'tasmania',
    'darwin': 'northern territory',
    'canberra': 'australian capital territory'
}

state_abbr = {
    'nsw': 'new south wales',
    'vic.': 'victoria',
    'qld': 'queensland',
    'sa': 'south australia',
    'wa': 'western australia',
    'tas.': 'tasmania',
    'nt': 'northern territory',
    'act': 'australian capital territory'
}

# get all file dirs
dir_path = 'data-geo/'
files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
save_path = '../data/twitter-geo.json'
file_paths = [dir_path + f for f in files]


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


# Extract the state name
def get_state(state):
    state = state.lower()
    if '(' in state:
        abbr = state[(state.index("(") + 1): -1]
        return state_abbr[abbr] if abbr in state_abbr.keys() else state
    return capitals[state] if state in capitals.keys() else state


def merge_and_save():
    pbar = tqdm(total=3226684, dynamic_ncols=True)
    # Open the output file in write mode
    with open(save_path, "wb") as output_file:
        # Write the opening square bracket for the merged JSON array
        # output_file.write("[")

        # Process each input file
        for index, file_name in enumerate(file_paths):
            with open(file_name, "r", encoding='utf-8') as input_file:
                # Use ijson to parse the JSON objects in the input file
                objects = ijson.items(input_file, "item")
                # Write each object to the output file
                for tweet in objects:
                    pbar.update()
                    if type(tweet['doc']['includes']) == list:
                        continue
                        # location = tweet['doc']['includes'][0]['full_name']
                    data = tweet['doc']['data']
                    location = tweet['doc']['includes']['places'][0]['full_name'].split(', ')
                    if len(location) == 0:
                        continue
                    item = None
                    if len(location) == 1 and location[0].lower() == 'australia':
                        item = {
                            'tokens': tweet['value']['tokens'],
                            'created_at': data['created_at'],
                            'lang': data['lang'],
                            'text': data['text'],
                            'sentiment': data['sentiment'],
                            'suburb': '',
                            'state': ''
                        }
                    elif len(location) == 2:
                        state = get_state(location[1])
                        if state not in states:
                            continue
                        item = {
                            'tokens': tweet['value']['tokens'],
                            'created_at': data['created_at'],
                            'lang': data['lang'],
                            'text': data['text'],
                            'sentiment': data['sentiment'],
                            'suburb': re.match(r'^([^(]+)', location[0]).group(1).strip().lower(),
                            'state': state
                        }
                    if item is not None:
                        item_data = json.dumps(item, cls=JSONEncoder, ensure_ascii=False).encode("utf-8")
                        output_file.write(item_data)
                        output_file.write(b",\n")

            # Remove the trailing comma and space after the last object
            if index == len(file_paths) - 1:
                output_file.seek(output_file.tell() - 2)
                output_file.truncate()
    pbar.close()


merge_and_save()
