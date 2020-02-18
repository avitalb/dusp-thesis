import pandas as pd 
import numpy as np 

def merge(voter_filename,data_filename,new_filename):
    voter_file = pd.read_csv(voter_filename)
    data_file = pd.read_csv(data_filename)
    # merge here, hardcode the column names for now
    merged = pd.merge(voter_file, data_file, left_on='county_ID', right_on='countyid', how="inner")
    return merged