import pandas as pd
import censusgeocode as cg
from tqdm import tqdm
from pandarallel import pandarallel

def geocode(f):
    df = pd.read_csv(f)
    df[tract] = df.parallel_apply(lambda x : geocode_util(x['RegStNum'],x['RegStName'],x['RegStType'],x['RegCity'],x['RegState'],x['RegZipCode']), axis=1) 
    print("df size before dropping null tracts",df.shape)
    df = df[df['tract'].notnull()]
    print("df size after dropping null tracts",df.shape)
    df.to_csv("results/2017_vouchers_voter_file_merged_geocoded.csv")

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

    print("geocode 2019")
    geocode(merged_2019)

    # print("geocode 2017")
    # geocode(merged_2019)