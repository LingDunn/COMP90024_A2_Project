import pandas as pd
import matplotlib.pyplot as plt


suburb_stats_dir = "suburb_stats/"

states_abbr = {
    'new south wales': 'nsw',
    'victoria': 'vic',
    'queensland': 'qld',
    'south australia': 'sa',
    'western australia': 'wa',
    'tasmania': 'tas',
    'northern territory': 'nt',
    'australian capital territory': 'act'
}


def suburb_features(topic_stats, suburb_stats):
    # load and merge
    topic_stats_df = pd.read_csv(topic_stats)
    suburb_stats_df = pd.read_csv(suburb_stats)

    merged_df = pd.merge(topic_stats_df, suburb_stats_df, on='suburb')
    merged_df = merged_df.drop(['min', 'max'], axis=1)

    fig, ax = plt.subplots(figsize=(20, 20))
    pd.plotting.scatter_matrix(merged_df, alpha=0.2, ax=ax)
    plt.show()

# suburb_features("suburb_stats/cc_nsw_suburb.csv", "sudo_gi/nsw.csv")


def suburb_stats(topic_stats, suburb_stats):
    # load and merge
    topic_stats_df = pd.read_csv(topic_stats)
    suburb_stats_df = pd.read_csv(suburb_stats)
    merged_df = pd.merge(topic_stats_df, suburb_stats_df, on='suburb')

    med_inc = merged_df["med_inc"].tolist()
    uni_rate = merged_df["uni_rate"].tolist()
    y12_rate = merged_df["y12_rate"].tolist()
    part_rate = merged_df["part_rate"].tolist()
    tafe_rate = merged_df["tafe_rate"].tolist()
    emp_rate = merged_df["emp_rate"].tolist()

    return med_inc, uni_rate, y12_rate, part_rate, tafe_rate, emp_rate


def histogram(data, bins, title, xlabel):
    plt.hist(data, bins=bins, color='skyblue')
    plt.xlabel(xlabel)
    plt.ylabel("Frequency")
    plt.title(title)
    plt.show()


res = suburb_stats("suburb_stats/cc_nsw_suburb.csv", "sudo_gi/nsw.csv")

histogram(res[0], 10, "med_inc", "Income")
