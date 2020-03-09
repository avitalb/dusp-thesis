import pandas as pd
import censusgeocode as cg
from tqdm import tqdm
from pandarallel import pandarallel
import censusbatchgeocoder

def geocode(f):
    df = pd.read_csv(f)
    #df[tract] = df.parallel_apply(lambda x : geocode_util(x['RegStNum'],x['RegStName'],x['RegStType'],x['RegCity'],x['RegState'],x['RegZipCode']), axis=1) 
    
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
    df = pd.merge(df,filtered_df,how="left",left_on = "address",right_on = "address")

    print("df size before dropping null tracts",df.shape)
    df = df[df['tract'].notnull()]
    print("df size after dropping null tracts",df.shape)
    df.to_csv("results/2017_vouchers_voter_file_merged_geocoded.csv")
    print("DONE")

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

    #df size before dropping null tracts (249085, 67)
    #df size after dropping null tracts (20545, 67)
    # print("geocode 2019")
    # geocode(merged_2019)

    #df size before dropping null tracts (27933, 72)
    #df size after dropping null tracts (10170, 72)
    print("geocode 2017")
    geocode(merged_2017)