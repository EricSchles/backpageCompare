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
cl = nbc(train)
for folder in folders:
    os.chdir(folder)
    df = pd.read_csv("ny_nj_data.csv")
    for 


