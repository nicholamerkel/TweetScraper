import pandas as pd
import glob
import json
import re
# from same blog post that recommended TweetScraper:
# https://www.simonlindgren.com/notes/2017/11/7/scrape-tweets-without-using-the-api

def main():
    files = glob.glob('Data/tweet/*')

    tweets = []
    for file in files:
        json_string = open(file, 'r').read()
        json_dict = json.loads(json_string)

        text = json_dict['text']
        text = re.sub(r'http\S+', '', text) # remove links
        text = re.sub(r'pic\.twitter\S+', '', text) # remove pictures
        if text == '': continue # if no text left... ignore that tweet!

        url = json_dict['url']
        cleaned_info= {
            'text' : text,
            'url' : url
        }
        tweets.append(cleaned_info)


    # have list of tweets. now want dataframe
    df = pd.DataFrame(tweets)

    df = df.replace({'\n': ' '}, regex=True) # remove linebreaks in the dataframe
    df = df.replace({'\t': ' '}, regex=True) # remove tabs in the dataframe
    df = df.replace({'\r': ' '}, regex=True) # remove carriage return in the dataframe
    df.to_excel("scraped/train_MASTER.xlsx", index=False)

main()
