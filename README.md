# CSE256-Final-Project
CSE256 Final Project

## Postive & Negative
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
2. 'length': text长度 (向上取整10)
3. 'source': 数据来源 (账号: 数量)
4. 'unigram': 出现次数最多的1000个单词
5. 'bigram': 出现次数最多的1000个Bigram
6. 'trigram': 出现次数最多的1000个Trigram

**TODO**: 单词难度分类
