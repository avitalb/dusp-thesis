import pandas as pd
import censusgeocode as cg
from tqdm import tqdm
from pandarallel import pandarallel

def geocode(f,seattle_acs,new_name):
    df = pd.read_csv(f)
    df['tract'] = df.parallel_apply(lambda x : geocode_util(x['RegStNum'],x['RegStName'],x['RegStType'],x['RegCity'],x['RegState'],x['RegZipCode']), axis=1) 
    print("df size before dropping null tracts",df.shape)
    df = df[df['tract'].notnull()]
    print("df size after dropping null tracts",df.shape)

    print("adding census tract income quintile rank for each address")
    df2 = seattle_acs
    df = pd.merge(df,df2[['TRACT','income_quintile']],left_on='tract',right_on="tract", how='left')


    df.to_csv(new_name)

def geocode_util(num,name,typ,city,state,zipcode):
    addr = str(num) + " " + str(name) + " " + str(typ)
    result = cg.address(addr, city=city, state=state, zipcode=zipcode,returntype='geographies')
    
    try:
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

    print("geocode 2019")
    geocode(merged_2019, df2,name_2019)

    print("geocode 2017")
    geocode(merged_2019, df2,name_2017)