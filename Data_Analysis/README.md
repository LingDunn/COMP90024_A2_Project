# COMP90024 - Data Analysis



## API

```
# Given a topic, return distributions over the country
/distribution/twitter/<string:topic>
http://172.26.135.213:5000/distribution/twitter/cc

# Given a topic and a state, return distributions over the state
/distribution/twitter/<string:topic>/<string:state>
http://172.26.135.213:5000/distribution/twitter/cc/new south wales

# Given a topic and a state, return topic_state_view
/view/twitter/<string:topic>/<string:state>
http://172.26.135.213:5000/view/twitter/cc/new south wales

# Get sudo gi data for a state
/sudo/gi/<string:state>
http://172.26.135.213:5000/sudo/gi/new south wales

# Get sudo avg data for a state
/sudo/avg/<string:state>
http://172.26.135.213:5000/sudo/avg/new south wales

# Get hashtags sorted by counts
# Limit the number of results returned
/hashtags/<int:limit>
http://172.26.135.213:5000/hashtags/1000

# Get view of mastodon data based on a topic
/view/mastodon/<string:topic>
http://172.26.135.213:5000/view/mastodon/cc

# Get view of twitter or mastodon data based on language
/view/lang/<string:db>
http://172.26.135.213:5000/view/lang/twitter
http://172.26.135.213:5000/view/lang/mastodon

# Get number of twitter or mastodon data
/count/<string:db>
http://172.26.135.213:5000/count/twitter
http://172.26.135.213:5000/count/mastodon

# Get number of counts of tweets quickly
/topic/count/twitter
http://172.26.135.213:5000/topic/count/twitter
```





## Twitter Data Analysis

### 1. Filter out data including location information

Run `mpiexec -n [#cores] python get_geo.py`

Generate n output files, including data with location information.

Outputs: `data-geo/twitter-geo{n}.json`



### 2. Merge and preprocess data

Run `python merge.py`

Save format: 

```json
{
    "tokens": "Last|year|40s|from|today|Derby|kind|please",
    "created_at": "2022-08-10T23:50:32.000Z", "lang": "en",
    "text": "Last year of my 40s from today. Derby be kind to me, please.",
    "sentiment": 0.23076923076923078,
    "suburb": "melbourne",
    "state": "victoria"
}
```

Output: `data/twitter-geo.json`



### 3. Retrieve related hashtags based on corpus of interested topics

Run `mpiexec -n [#cores] python hashtag.py`

Save all hashtags: `hashtags/hashtags.csv`

Save all hashtags with counts: `hashtags/hashtags-cnt.json`

Use `topic-tag.py` to retrieve related hashtags based on corpus of interested topics.



### 4. Classify data into topics

#### Topics

* Politics

  * Scotty Morrison

  * Ukraine

* Web3

  * Cryptocurrency

  * NFT

* Pornographic

Run `mpiexec -n [#cores] python get_topic_tag.py`

Extract hashtags and perform topic classification

Save format:

```json
{
    "tokens": "Presenting|HUMBLEBEE|Link|profile|page",
    "created_at": "2022-02-10T00:59:41.000Z",
    "lang": "en",
    "text": "@i_sunshine_9 Presenting HUMBLEBEE V2\n#nftart #nftsale #NFTCommunity #NFTs \nLink on profile page to @opensea ---------------------------\nhttps://t.co/HhkdBcK7T7",
    "sentiment": 0.09523809523809523,
    "suburb": "melbourne",
    "state": "victoria",
    "tag": ["#nftart", "#nftsale", "#nftcommunity", "#nfts"],
    "topic": ["web3"],
    "sub_topic": ["nft"]
}
```

Output: `data/twitter-topic.json`



## SAL & SUDO

### SAL

Run `python sal.py`

Save format:

```json
{
    "state": "new south wales",
    "suburbs": [suburbs]
}
```

Output: `data/state-suburb.json`



### SUDO

#### Dataset:

* `GI_-_Working_Age_Employment_and_Income__Suburb__2011`

* `Selected_Medians_and_Averages`

Run `python sudo.py`

##### Outputs:

* `sudo/state-avg.json`

  * Columns

    ```
    GCCSA code 2021
    Median age of persons
    Median mortage repayment ($/monthly)
    Median total personal income ($/weekly)
    Median rent ($/weekly)
    Median total family income ($/weekly)
    Average number of persons per bedroom
    Median total household income ($/weekly)
    Average household size
    ```

  * Save format:

    ```json
    {
        "gcc": "1GSYD",
        "med_age": 37,
        "med_month_mortgage": 2427,
        "med_week_inc": 881,
        "med_week_rent": 470,
        "med_week_fam_inc": 2374,
        "avg_num_psn_per_bd": 0.9,
        "med_week_hhd_inc": 2077,
        "avg_hhd_size": 2.7
    }
    ```

* `sudo/suburb-stat.json`

  * Columns

    ```
    State
    Suburb
    Median incomes of individual aged 25-65 (2011 dollars)
    Proportion of popluation with a bachelor degree or higher
    Proportion of popluation with no post-school qualifications
    Participation rate (labour force as a proportion to the population)
    Proportion of popluation with TAFE qualification. E.g. Cert 3/4, diploma
    Total number of inidividuals employed as a proportion to the total population
    Female participation rate (labour force as a proportion to the population)
    Male participation rate (labour force as a proportion to the population)
    Difference between male and female participation rates
    ```

  * Save format:

    ```json
    {
        "state": "new south wales",
        "suburb": "abbotsbury",
        "med_inc": "42926.78788",
        "uni_rate": "0.182964",
        "y12_rate": "0.472838",
        "part_rate": "0.816838",
        "tafe_rate": "0.344198",
        "emp_rate": "0.769665",
        "female_part": "0.737489",
        "male_part": "0.900274",
        "part_less": "0.162785"
    }
    ```




## CouchDB

### Insert data

Use `insert.py`

Create a new database: `create_db`

Small json file: `insert_bulk`

Large json file: `insert_batch_bulk`

