# thesis
MIT DUSP 2020 Undergraduate Thesis - analysis of Seattle Democracy Vouchers Program data

# Workflow
The workflow is separated between handling the Vouchers data (data of redeemed Democracy Vouchers) 
and handling the data from the cash contributions (data of direction donations to campaigns, outside of the Democracy Vouchers program). Each of the files runs the given tasks for both the 2017 and 2019 dataset. 

## Vouchers Data Wrangling

1) run `merge.py` to merge voter file and voucher file and add age buckets as follow:

1: 18–29
2: 30–44,
3: 45–59
4: 60 years or older

(making sure to remove duplicates as participants can donate multiple democracy vouchers)

2) run `geocoding.py` to geocode addresses and add their respective census tracts to the csv

3) run `census_tracts_calc.py` to assign an income quintile to each entry, using their census tract

4) run `add_ethnicity.py` to query the [NamePrism API](http://www.name-prism.com/) to get an estimated ethnicity for the name of each entry (will need to read up more about how accurate this API is)

5) run `final_merge.py` to merge all these calculations into one big spreadsheet, whose name contains the year ending with "all_cols"

6) run `plotting.py` to make graphs of the data

## Cash Contributions Data Wrangling
1) run `cash_contributions.py` to merge the voter file and the cash contributions, and add age calculation and age bucket for each entry (making sure to remove duplicates)