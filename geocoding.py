import pandas as pd
import censusgeocode as cg
from tqdm import tqdm
from pandarallel import pandarallel
import time
import censusbatchgeocoder

def geocode(f,seattle_acs,new_name):
    df = pd.read_csv(f)

    df['RegStNum'] = df['RegStNum'].apply(str) 
    print("got here")
    df['address'] = df['RegStNum'] + " " + df['RegStName'] + " " + df['RegStType']
    df['city'] = df['RegCity'].copy()
    df['state'] = df['RegState'].copy()
    df['zipcode'] = df['RegZipCode'].copy()
    df['id'] = df.index

    filtered_df = df[['address',"city","state","zipcode","id"]]

    result = censusbatchgeocoder.geocode(filtered_df.to_dict("records"))
    filtered_df= pd.DataFrame(result)
    df = pd.merge(df,filtered_df[['address','tract']],how="left",left_on = "address",right_on = "address")

    print("df size before dropping null tracts",df.shape)
    df = df[df['tract'].notnull()]
    print("df size after dropping null tracts",df.shape)

    print("adding census tract income quintile rank for each address")
    df2 = seattle_acs

    # make both tract columns ints to avoid this error:  "ValueError: You are trying to merge on object and int64 columns. If you wish to proceed you should use pd.concat"
    df["tract"] = df["tract"].astype(int)

    
    df = pd.merge(df,df2[['TRACT','income_quintile']],left_on='tract',right_on="TRACT", how='left')

    df.to_csv(new_name)

    print("DONE")

    # tqdm.pandas()
    # df = pd.read_csv(f)
    # df['tract'] = df.progress_apply(lambda x : geocode_util(x['RegStNum'],x['RegStName'],x['RegStType'],x['RegCity'],x['RegState'],x['RegZipCode']), axis=1) 
    # print("df size before dropping null tracts",df.shape)
    # df = df[df['tract'].notnull()]
    # print("df size after dropping null tracts",df.shape)

def geocode_util(num,name,typ,city,state,zipcode):
    # time.sleep(1)
    addr = str(num) + " " + str(name) + " " + str(typ)
    try:
        result = cg.address(addr, city=city, state=state, zipcode=zipcode,returntype='geographies')
        tract = result[0]['geographies']['Census Tracts'][0]['GEOID']
    except:
        tract = None
    return tract 

if __name__ == '__main__':
    pandarallel.initialize(progress_bar = True)
    merged_2019 = "results/2019_vouchers_voter_file_merged.csv"
    merged_2017 = "results/2017_vouchers_voter_file_merged.csv"

    name_2019 = "results/2019_vouchers_voter_file_merged_geocoded.csv"
    name_2017 = "results/2017_vouchers_voter_file_merged_geocoded.csv"

    seattle_acs = "results/seattle_acs.csv"
    df2 = pd.read_csv(seattle_acs)

    print("geocode 2019 vouchers")
    # df size before dropping null tracts (249085, 51)
    # df size after dropping null tracts (20549, 51)
    geocode(merged_2019, df2,name_2019)

    print("geocode 2017 vouchers")
    geocode(merged_2019, df2,name_2017)

    print("geocode 2019 cash")
    geocode("results/2019_cash_merged.csv", df2,"results/2019_cash_ethnicity_merged_geocoded.csv")

    print("geocode 2017 cash")
    geocode("results/2017_cash_merged.csv", df2,"results/2017_cash_ethnicity_merged_geocoded.csv")
