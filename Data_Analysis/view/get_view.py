import requests
import json
import csv


username = 'admin'
password = 'admin'
server = '172.26.135.87:5984'
db_name = 'twitter-geo'

state_dir = "state_stats/"
suburb_dir = "suburb_stats/"


def save_view_stats(view_name, filename, state=False):
    url = f"http://{username}:{password}@{server}/{db_name}/_design/{view_name}/_view/{view_name}"
    params = {'group_level': 1}
    response = requests.get(url, params=params)
    data = response.json()
    res = []
    res.append(['state', 'count', 'min', 'max', 'avg']) if state else res.append(['suburb', 'count', 'min', 'max', 'avg'])

    for row in data['rows']:
        loc = row['key']
        if loc == "":
            continue
        value = row['value']
        # The 'value' object contains 'count', 'sum', 'min', 'max', 'sumsqr'
        count = value['count']
        total = value['sum']
        min_sentiment = value['min']
        max_sentiment = value['max']
        avg_sentiment = total / count
        res.append([loc, count, min_sentiment, max_sentiment, avg_sentiment])

    save_dir = state_dir if state else suburb_dir
    with open(f"{save_dir}{filename}.csv", 'w', newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow(res[0])
        writer.writerows(res[1:])
    file.close()


def get_design_docs():
    url = f"http://{username}:{password}@{server}/{db_name}/_design_docs"
    response = requests.get(url)
    data = response.json()
    for row in data['rows']:
        view_name = row['id'][8:]
        if "state" in view_name:
            save_view_stats(view_name, view_name, state=True)
        else:
            save_view_stats(view_name, view_name)


get_design_docs()
