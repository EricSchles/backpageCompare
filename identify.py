from textblob.classifiers import NaiveBayesClassifier as nbc
import pandas as pd
import time
from glob import glob
from sys import argv
import pickle
website = argv[1]
folders = glob(website+"*")

#add training data here
training = pickle.load("training")
keywords = pickle.load("keywords")
emails = pickle.load("emails")
phone_numbers = pickle.load("phone_numbers")
cl = nbc(train)
positive = pd.DataFrame()
negative = pd.DataFrame()
for folder in folders:
    os.chdir(folder)
    df = pd.read_csv("ny_nj_data.csv")
    for ind,line in enumerate(df["body"]):
        for email in emails:
            if email in line:
                positive.append(df.iloc[ind],ignore_index=True)
        for phone_number in phone_numbers:
            if phone_number in df.iloc[ind]["phone_number"]:
                positive.append(df.iloc[ind],ignore_index=True)
        common_keywords = []
        for keyword in keywords:
            if keyword in line:
                common_keywords.append(keyword)
        
        result = cl.classify(line)
        if result == "pos":
            positive = positive.append(df.iloc[ind],ignore_index=True)
        if result == "neg":
            negative = negative.append(df.iloc[ind],ignore_index=True)
    os.chdir("../")
positive.to_csv("positive.csv")
negative.to_csv("negative.csv")

