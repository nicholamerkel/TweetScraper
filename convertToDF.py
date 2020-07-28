import pandas as pd
import string
import glob
import json
import re
import argparse

# from same blog post that recommended TweetScraper:
# https://www.simonlindgren.com/notes/2017/11/7/scrape-tweets-without-using-the-api

def main(args):
    filename = args['filename']
    cleanText = args['cleanText']
    files = glob.glob('Data/tweet/*')

    tweets = []
    for file in files:
        json_string = open(file, 'r').read()
        json_dict = json.loads(json_string)

        text = json_dict['text']
        text = re.sub(r'http.+', '', text) # remove links
        text = re.sub(r'pic\.twitter\S+', '', text) # remove links to pictures
        if text == '': continue # if no text left... ignore that tweet!

        if cleanText: # specified to clean text (but keep both)
            cleaned = text.lower()
            cleaned = re.sub(r'@#\S*', '', cleaned) # remove mentions and hashtags
            cleaned = re.sub(r'[()\"\'\\/_-]', '', cleaned) # removes quotations,underscores,forward and backslash, etc. just keeps sentence punctuation
            # cleaned = re.sub(r'[^\w\s]', '', cleaned) # remove punctuation (including @ and # for mentions and RTs)
            info = {
                'text' : text,
                'cleanedText' : cleanedText
            }
        else:
            info = {
                'text' : text
            }
        tweets.append(info)


    # have list of tweets. now want dataframe
    df = pd.DataFrame(tweets)

    df = df.replace({'\n': ' '}, regex=True) # remove linebreaks in the dataframe
    df = df.replace({'\t': ' '}, regex=True) # remove tabs in the dataframe
    df = df.replace({'\r': ' '}, regex=True) # remove carriage return in the dataframe
    df.to_excel(f"scraped/{filename}", index=False)
    print(f"tweets ready. file can be found at: scraped/{filename}")
    if cleanText: print("in format: <originalTweetText> <cleaned tweet text>")
    else: print("in format: <originalTweetText>")

if __name__ ==  '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("--filename", required=True, type=str, help="specify filename to write to")
    ap.add_argument("--cleanText", default=False, action='store_true', help="keep original text but also includes clean version (ie. without unneccessary punctuation, mentions, hashtags). note, links to websites/photos will always be removed from text")

    args = vars(ap.parse_args())
    main(args)
