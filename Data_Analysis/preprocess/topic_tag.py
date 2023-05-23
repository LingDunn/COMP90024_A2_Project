import csv


corpus_web3_path = '../corpus/web3.csv'
corpus_politics_path = '../corpus/politics.csv'
corpus_porn_path = '../corpus/porn.csv'
# corpus_sports_path = 'corpus/sports.csv'
corpus_paths = [corpus_web3_path,
                corpus_politics_path,
                corpus_porn_path]


def get_tag(corpus_path, save_path):
    with open('../hashtag/hashtags.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        hashtags = next(reader)

    with open(corpus_path, 'r', encoding='utf-8') as f:
        corpus = [w.lower() for w in next(csv.reader(f))]

    res = []
    for word in corpus:
        for hashtag in hashtags:
            if word in hashtag:
                res.append(hashtag)

    with open(save_path, 'w', newline='', encoding='utf-8') as fp:
        writer = csv.writer(fp)
        writer.writerow(res)


# get_tag(corpus_web3_path, "hashtag/web3.csv")
# get_tag(corpus_politics_path, "hashtag/politics.csv")
# get_tag(corpus_porn_path, "hashtag/porn.csv")
# get_tag('corpus/politics/scotty.csv', "hashtag/politics/scotty.csv")
# get_tag('corpus/politics/ukraine.csv', "hashtag/politics/ukraine.csv")
# get_tag('corpus/web3/cryptocurrency.csv', "hashtag/web3/cryptocurrency.csv")
# get_tag('corpus/web3/nft.csv', "hashtag/web3/nft.csv")
