import pandas as pd
import glob
import json
import re

def main():
    files = glob.glob('Data/tweet/*')
    print(len(files))


    dictlist = []
    for file in files:
        json_string = open(file, 'r').read()
        json_dict = json.loads(json_string)

        text = json_dict['text']
        text = re.sub(r'http\S+', '', text) # remove links
        text = re.sub(r'pic\.twitter\S+', '', text) # remove pictures
        if text == '': continue # if no text left... ignore that tweet!

        url = json_dict['url']
        cleaned_dict = {
            'text' : text,
            'url' : url
        }
        dictlist.append(cleaned_dict)


    # have list of tweets. now want dataframe
    df = pd.DataFrame(dictlist)

    df = df.replace({'\n': ' '}, regex=True) # remove linebreaks in the dataframe
    df = df.replace({'\t': ' '}, regex=True) # remove tabs in the dataframe
    df = df.replace({'\r': ' '}, regex=True) # remove carriage return in the dataframe
    df.to_excel("scraped/train_MASTER.xlsx", index=False)

main()
