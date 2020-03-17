import pandas as pd 
import numpy as np 
import datetime

# reference date in datetime format, birthdate in %Y-%m-%d format, 
def get_age(ref_date,born):
    born = datetime.datetime.strptime(born, '%Y-%m-%d')
    return ref_date.year - born.year - ((ref_date.month, ref_date.day) < (born.month, born.day))

# age buckets from McCabe/Herwig  
# 1: 18–29
# 2: 30–44,
# 3: 45–59
# 4: 60 years or older.
def get_age_bucket(age):
    if age <= 29:
        return 1
    elif age <= 44:
        return 2
    elif age <= 59:
        return 3
    else:
        return 4

def reformat_voucher_file(year):
    filename = ""
    if year == 2019:
        filename = "/Users/abaral/src/thesis/2019_final_dvp_data_raw.csv"
    elif year == 2017:
        filename = "/Users/abaral/src/thesis/2017_final_dvp_data_raw.csv"
    data_file = pd.read_csv(filename)
    data_file.rename(columns = {'Participant ID (Participant) (Contact)':'participant_id'}, inplace = True) 
    if year == 2019:
        data_file.to_csv("results/2019_voucher_file_formatted.csv")
    elif year == 2017:
        data_file.to_csv("results/2017_voucher_file_formatted.csv")