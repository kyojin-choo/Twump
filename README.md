# Twump

Twump aims to do three big things.
1. Scrape a user's Twitter.
2. Map and Reduce the JSONs outputted from the scraper.
3. Perform NLP and K-NN on two datasets--one always being @realDonaldTrump and another user.

The idea is to compare @realDonaldTrump, the impeached 45th President of the United States, tweets to other users on Twitter. This project is merely just for fun; it is interesting to see the similarities between Donald Trump's tweets and another user's tweets. I am not trying to disparage or tarnish other people's names or  Even if this project finds a correlation, that is not definitively the truth, meaning that if one's tweets are similar to Donald Trump this does not reflect a similarity in their ideologies, philosophies, and other beliefs.

## Requirements
- Python 3.7
- Tweepy
  - This is mandatory to execute extract.py as a Twitter Developer's Account is necessary to access Twitter's REST API.
- Hadoop 
  - Required only if MapReduce functions want to be executed. For this project, I have used a single-node setup, using my computer as the single node.
  - Any MapReduce files will still work when executed when you are not in the HDFS, but it obviously will not queue jobs.
  
## Extract.py (Tweepy)
- 
