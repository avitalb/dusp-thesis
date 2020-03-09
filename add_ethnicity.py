import pandas as pd
import requests 
from tqdm import tqdm

API_KEY = "f9832b6322bc14f4"

def add_ethnicity(f,new_name):
    tqdm.pandas()
    df = pd.read_csv(f)
    df["est_ethnicity"] = df.progress_apply(lambda x : make_request(x['FName'],x['LName']), axis=1) 
    df.to_csv(new_name)

def make_request(first_name, last_name):
    url = "http://www.name-prism.com/api_token/eth/json/" + API_KEY + "/" + first_name + "%20" + last_name
    r = requests.get(url = url, params = {})
    data = r.json()
    to_return = ""
    current_max = 0

    for opt in data:
        if data[opt] > current_max:
            current_max = data[opt]
            to_return = opt
    return to_return

if __name__ == '__main__':
    merged_2019 = "results/2019_vouchers_voter_file_merged.csv"
    merged_2017 = "results/2017_vouchers_voter_file_merged.csv"
    new_2019_name = "results/2019_vouchers_voter_file_ethnicity.csv"
    new_2017_name = "results/2017_vouchers_voter_file_ethnicity.csv"

    print("add ethnicity for 2019")
    add_ethnicity(merged_2019,new_2019_name)

    print("add ethnicity for 2017")
    add_ethnicity(merged_2017,new_2017_name)