import pandas as pd 
import utils
import datetime

# PACs/groups that are NOT for municipal candidates - 2019 election
NON_MUN_CAND_2019 = ['Alliance 4 Gun Responsibility', 'Civ Alliance (CASE)',
       'CivicAlliance4Prog Economy', 'Dist 1 Nbrs for Sm Bus.',
       'MBA KING & SNO - Affordable', 'Moms For Seattle',
       'NATIVE WOMEN&#39;S PAC', 'NBRHDS FOR SMART STREETS PAC', 'PALS',
       'PEOPLE FOR SEATTLE', 'Sea Hosp 4 Progress PAC',
       'SEATTLE FIRE FIGHTERS PAC', 'Seattle Neighborhood Council',
       'SEIU HLTHCARE775 QualCareCmte', 'UNITE HERE Local 8 PAC',
       'UNITE HERE TIP', 'WkgPpl4Affordable Seattle',
       'FAIRVOTE WA FOR SEATTLE CA-27',
       'Accountability 4 Seattle',  'YESSEATTLELIBRARIES']

# PACs/groups that are NOT for municipal candidates - 2017 election
NON_MUN_CAND_2017 = ['Affordable Seattle', 'FUSE VOTES',
       'Master Builders - Affdbl Housn', 
       'PLANNED PRNTHD VOTESNW WA PAC', 'HEATS',
       'REDUCE SEA HOMELESSNESS NOW', 'Seattleites for Rent Transpare',
       'BACK TO BASICS COMM', 
       'COAL. FOR HLTHY KIDS & ED']
       
# merging voter file to contributions file (fuzzy name matching)
def merge_cash(voter_filename,data_filename,new_filename,year):
    ref_date = 0
    if year == 2019:
        # last day to designate vouchers for 2019 was November 29, 2019
        ref_date = datetime.date(2019,11,29)
    elif year == 2017:
        # last day to designate vouchers for 2017 was December 1st, 2017
        ref_date = datetime.date(2017,12,1)

    voter_file = pd.read_csv(voter_filename,sep='|',encoding = "cp1252")
    data_file = pd.read_csv(data_filename)
    
    print("voter file",voter_file.head())
    print("data file",data_file.head())

    # keep only the transactions noted C3.2 (contributions)
    data_file = data_file[data_file.strPDCFormLineNumber == "C3.2"]

    # drop duplicates and irrelevant donations based on list above
    if year == 2019:
        data_file = data_file[~data_file.strCampaignName.isin(NON_MUN_CAND_2019)]
    elif year == 2017:
        data_file = data_file[~data_file.strCampaignName.isin(NON_MUN_CAND_2017)]

    data_file.drop_duplicates(subset=['intLinkID_SEEC'])

    print("voter file shape",voter_file.shape)
    print("donor file shape",data_file.shape)

    # in donor file, add first and last name columns to prepare for matching with voter file
    name_split = data_file["strTransactorName"].str.split()
    data_file['first_name'] = name_split.str[0]
    data_file['last_name'] = name_split.str[-1]

    # merge on last name, first name, zipcode, and street number (see McCabe/Herwig appendix)
    merged = pd.merge(data_file, voter_file,  
        left_on=['first_name','last_name','strCity','strZip'], right_on=['FName','LName','RegCity','RegZipCode'], how="inner")
    print("merged",merged.head())
    print("merged size",merged.shape)

    merged['age'] = merged.apply(lambda x: utils.get_age(ref_date, x['Birthdate']),axis=1)
    merged['age_bucket'] = merged.apply(lambda x : utils.get_age_bucket(x['age']), axis=1) 

    merged.to_csv(new_filename)
    return merged


# cash contributions pipeline
if __name__ == "__main__":
    cash_2019 = "2019_contributors.csv"
    cash_2017 = "2017_contributors.csv"

    voter_file = "/Users/abaral/src/thesis/wa_voter_file_02_19_2020/202002_VRDB_Extract.txt"

    new_name_2019 = "results/2019_cash_merged.csv"
    new_name_2017 = "results/2017_cash_merged.csv"

    print("merging 2019 cash contributions with voter file, adding age")
    # voter file shape (4921002, 35)
    # donor file shape (65638, 27)
    # merged size (22534, 64)
    merge_cash(voter_file,cash_2019,new_name_2019,2019)

    print("merging 2017 cash contributions with voter file, adding age")
    # voter file shape (4921002, 35)
    # donor file shape (38637, 27)
    # merged size (6602, 64)
    merge_cash(voter_file,cash_2017,new_name_2017,2017)



