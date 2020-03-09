import pandas as pd 


def get_seattle_acs_quintiles(tracts,acs):
    acs = pd.read_csv(acs)
    tracts = pd.read_csv(tracts)

    # extract only seattle acs data
    seattle_acs = pd.merge(tracts,acs,left_on="GEOID10", right_on="GEOID10", how="left")

    #make 5 income quintiles
    seattle_acs['income_quintile'] = pd.qcut(seattle_acs['MEDIAN_HH_INC_PAST_12MO_DOLLAR'], q=5, precision=0,labels=["bottom", "fourth", "middle","second","top"])

    seattle_acs.to_csv("results/seattle_acs.csv")

    condensed = seattle_acs[['TRACTCE10','NAME10','GEOID10', 'MEDIAN_HH_INC_PAST_12MO_DOLLAR', 'income_quintile']].copy()
    condensed.to_csv("results/tracts_income.csv")

if __name__ == '__main__':
    tracts = "seattle_census_tracts.csv"
    acs = "king_county_acs.csv"
    get_seattle_acs_quintiles(tracts,acs)