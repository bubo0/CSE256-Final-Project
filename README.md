# CSE256-Final-Project
CSE256 Final Project

## Positive & Negative
### Resources

Cached data and trained classifier

### Untitled.ipynb

Playground for writting the py scripts that get triggered when user submit a request.

## Trump

### Data
1. {}_tweets.csv 文件是api刮下来的， 但是由于不知名限制只能每个账号回溯2000+tweets。
2. MORE_TRUMP.csv是由一个Trump tweets archive下载来的，有完整的数据，现截取了2016开始的，大约10000条。
3. 以上都不含native tweets。(无内容的retweets)

### dataset_statistic.json
>数据集的相关分析,包括
1. 'count': 数据量 (total, Trump, not Trump, validation)
2. 'length': text长度列表
3. 'source': 数据来源 (账号: 数量)
4. 'unigram': 出现次数最多的10个单词和最少的10个单词
5. 'bigram': 出现次数最多的10个Bigram和最少的10个Bigram
6. 'trigram': 出现次数最多的10个Trigram和最少的10个Trigram

### words_level.json
Tweets使用单词级别统计,格式如下
```
{
    "realDonaldTrump": {
        "TOEFL": 0.3483347680749494,
        "others": 0.176213288315986,
        "primary": 0.4286085614945163,
        "GRE": 0.04684338211454828
    },
    ... ...
}
```

### performance.json
>参数调试,包括Vectorizer,Ngram,min_df,max_df (lowercase都是false比较好,结果没有放进来)

最佳模型的score

格式如下:
```
{
    {
        "Vectorizer": "Count",
        "lowercase": "False",
        "score": { //最佳模型score
            "accuracy": 0.9441323345817728,
            "recall": 0.9411388355726168,
            "precision": 0.9441591784338896,
            "f1": 0.9426465876321692
        },
        "ngram": { //调试变量
            "1": "0.928214732", //对应performance
            "2": "0.941635456",
            "3": "0.944132335",
            "4": "0.940699126",
            "5": "0.938826467",
            "6": "0.937578027",
            "7": "0.937265918",
            "8": "0.936017478",
            "9": "0.935393258"
        },       
        ... ... 
    },
   ... ...
}
```
### example_instances.json
most confident true positive/negative 和 most overconfident false postive/negative 的10个例子
```
{
    "true Trump": {
        "JimRenacci has worked so hard on Tax Reductions Illegal Immigration the Border and Crime.": [
            1.4794265146278462e-08,
            0.9999999852057349
        ],
        ... ...
    }
    ... ...
}
```
