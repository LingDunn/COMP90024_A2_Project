import re
import ijson
from collections import defaultdict


sal_path = "../data/sal.json"
save_path = "../data/state-suburb.json"
states = ['new south wales',
          'victoria',
          'queensland',
          'south australia',
          'western australia',
          'tasmania',
          'northern territory',
          'australian capital territory'
          ]


# Load and process sal.json
def load_sal(fp):
    data = defaultdict(list)
    with open(fp, 'r', encoding='utf-8') as fp:
        suburbs_data = ijson.items(fp, '')
        for suburbs in suburbs_data:
            for suburb, values in suburbs.items():
                sub = re.match(r'^([^(]+)', suburb).group(1).strip().lower()
                gcc = values['gcc']
                if values['ste'] != "9":
                    data[states[int(gcc[0]) - 1]].append(sub)
    return data


def get_au_state_suburb(file_path):
    au_state_suburb = load_sal(sal_path)
    with open(file_path, 'w') as output_file:
        cnt = 0
        for key, suburbs in au_state_suburb.items():
            data = f'''"state": "{key}", "suburbs": ['''
            for i, sub in enumerate(suburbs):
                data += f'''"{sub}"'''
                if i < len(suburbs) - 1:
                    data += ", "
            data = "{" + data + "]}"
            if cnt < 7:
                data += ",\n"
            output_file.write(data)
            cnt += 1


get_au_state_suburb(save_path)
