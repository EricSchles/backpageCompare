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
    found_emails = []
    found_numbers = []
    for ind,line in enumerate(df["body"]):
        for email in emails:
            if email in line:
                found_emails.append(email)
                email_result = True
                positive.append(df.iloc[ind],ignore_index=True)
        for phone_number in phone_numbers:
            if phone_number in df.iloc[ind]["phone_number"]:
                found_numbers.append(phone_number)
                phone_number_result = True
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
        with open("analysis.txt","a") as f:
            f.write("for the record: "+line+"\n")
            f.write("the following keywords were found:\n"+common_keywords+"\n")
            f.write("the naive bayesian classifier, which compares text to determine if they are similar, (pos) means similar, (neg) means dissimilar: "+result+"\n")
            if email_result:
                f.write("\nThe following email(s) was found in the ad:\n")
                f.write(found_emails)
            else:
                f.write("\nAn email address from the list was not found\n")
            if phone_number_result:
                f.write("\nThe following phone number(s) was found in the ad:\n")
                f.write(found_numbers)
    os.chdir("../")

positive.to_csv("positive.csv")
negative.to_csv("negative.csv")

