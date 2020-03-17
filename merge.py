import pandas as pd 
import numpy as np 
import datetime
import utils

# merging voter file to contributions file (fuzzy name matching)
# def merge(voter_filename,data_filename,new_filename):
#     voter_file = pd.read_csv(voter_filename,sep='|',encoding = "cp1252")
#     data_file = pd.read_csv(data_filename)

#     print("voter file",voter_file.head())
#     print("data file",data_file.head())

#     # rename donor file column 
#     data_file.rename(columns = {'Participant ID (Participant) (Contact)':'participant_id'}, inplace = True) 

#     print("voter file columns",voter_file.columns)
#     print("donor file columns",data_file.columns)
#     voter_file.to_csv("voter_file_formatted.csv")

#     # print # of rows and columns in voter file and donor file
#     print("voter file shape",voter_file.shape)
#     print("donor file shape",data_file.shape)

#     # drop duplicates in donor file, to get people who used >= 1 democracy voucher
#     vouchers_no_dups = data_file.drop_duplicates(subset="participant_id")
#     print("size of no dups file",vouchers_no_dups.shape)
#     print("vouchers no dups",vouchers_no_dups.head())

#     # in donor file, add first and last name columns to prepare for matching with voter file
#     name_split = vouchers_no_dups["Participant"].split()
#     vouchers_no_dups['first_name'] = name_split.str[0]
#     vouchers_no_dups['last_name'] = name_split.str[-1]

#     # merge on last name, first name, zipcode, and street number (see McCabe/Herwig appendix)
#     # hardcode column names for now
#     merged = pd.merge(vouchers_no_dups, voter_file,  
#         left_on=['first_name','last_name'], right_on=['FName','LName'], how="inner")
#     print("merged",merged.head())
#     print("merged size",merged.shape)
#     merged.to_csv(new_filename)
#     return merged


# merging voucher data (can use washington stateid)
def merge_voucher_data(voter_filename,data_filename,new_filename,year):
    ref_date = 0
    col_name = ""
    if year == 2019:
        # last day to designate vouchers for 2019 was November 29, 2019
        ref_date = datetime.date(2019,11,29)
        col_name = 'Participant ID (Participant) (Contact)'
    elif year == 2017:
        # last day to designate vouchers for 2017 was December 1st, 2017
        ref_date = datetime.date(2017,12,1)
        col_name = 'Participant ID (Participant)'
    voter_file = pd.read_csv(voter_filename,sep='|',encoding = "cp1252")
    data_file = pd.read_csv(data_filename)

    # rename donor file column 
    data_file.rename(columns = {col_name:'participant_id'}, inplace = True) 

    print("voter file",voter_file.head())
    print("data file",data_file.head())

    # print # of rows and columns in voter file and donor file
    print("voter file shape",voter_file.shape)
    print("donor file shape",data_file.shape)

    # drop duplicates in donor file, to get people who used >= 1 democracy voucher
    vouchers_no_dups = data_file.drop_duplicates(subset="participant_id")
    print("size of no dups file",vouchers_no_dups.shape)
    print("vouchers no dups",vouchers_no_dups.head())

    # merge on participant_id and StateVoterID
    merged = pd.merge(vouchers_no_dups, voter_file,  
        left_on='participant_id', right_on='StateVoterID', how="inner")
    print("merged",merged.head())
    print("merged size",merged.shape)

    # add raw_age column and put in age buckets
    merged['age'] = merged.apply(lambda x: utils.get_age(ref_date, x['Birthdate']),axis=1)
    merged['age_bucket'] = merged.apply(lambda x : utils.get_age_bucket(x['age']), axis=1) 

    merged.to_csv(new_filename)
    return merged

if __name__ == '__main__':
    # print("reformatting the voter file")
    # utils.reformat_voucher_file(2019)
    # utils.reformat_voucher_file(2017)

    print("merging 2020 voter file with 2019 dvp data")
    data_file_2019_voucher = "/Users/abaral/src/thesis/results/2019_voucher_file_formatted.csv"
    voter_file = "/Users/abaral/src/thesis/wa_voter_file_02_19_2020/202002_VRDB_Extract.txt"
    merge_voucher_data(voter_file,data_file_2019_voucher,"results/2019_vouchers_voter_file_merged.csv",2019)

    print("merging 2020 voter file with 2017 dvp data")
    data_file_2017_voucher = "/Users/abaral/src/thesis/results/2017_voucher_file_formatted.csv"
    voter_file = "/Users/abaral/src/thesis/wa_voter_file_02_19_2020/202002_VRDB_Extract.txt"
    merge_voucher_data(voter_file,data_file_2017_voucher,"results/2017_vouchers_voter_file_merged.csv",2017)
