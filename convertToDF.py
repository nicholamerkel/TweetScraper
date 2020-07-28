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
    removeUncleanedText = args['removeUncleanedText']
    files = glob.glob('Data/tweet/*')

    tweets = []
    for file in files:
        json_string = open(file, 'r').read()
        json_dict = json.loads(json_string)

        text = json_dict['text']
        cleanedText = text.lower()
        cleanedText = re.sub(r'http.+', '', cleanedText) # remove links
        cleanedText = re.sub(r'pic\.twitter\S+', '', cleanedText) # remove links to pictures
        cleanedText = re.sub(r'@#\S*', '', cleanedText) # remove mentions and hashtags
        cleanedText = re.sub(r'[\"\'\\/_-]', '', cleanedText) # removes quotations,underscores,forward and backslash, etc. just keeps sentence punctuation
        # cleanedText = re.sub(r'[^\w\s]', '', cleanedText) # remove punctuation (including @ and # for mentions and RTs)

        if cleanedText == '': continue # if no text left... ignore that tweet!

        if removeUncleanedText:
            info = {
                'cleanedText' : cleanedText
            }
        else: # keep uncleaned, unformatted text (ie. original tweet text)
            info = {
                'text' : text,
                'cleanedText' : cleanedText
            }
        tweets.append(info)


    # have list of tweets. now want dataframe
    df = pd.DataFrame(tweets)

    df = df.replace({'\n': ' '}, regex=True) # remove linebreaks in the dataframe
    df = df.replace({'\t': ' '}, regex=True) # remove tabs in the dataframe
    df = df.replace({'\r': ' '}, regex=True) # remove carriage return in the dataframe
    df.to_excel(f"scraped/{filename}", index=False)
    print(f"tweets ready. file can be found at: scraped/{filename}")
    if removeUncleanedText: print("in format: <cleaned tweet text>")
    else: print("in format: <cleanedTweetText> <originalTweetText>")

if __name__ ==  '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("--filename", required=True, type=str, help="specify filename to write to")
    ap.add_argument("--removeUncleanedText", default=False, action='store_true', help="flag specifies that uncleaned text from tweet will be discarded")

    args = vars(ap.parse_args())
    main(args)
