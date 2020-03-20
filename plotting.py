import pandas as pd 
import matplotlib.pyplot as plt

def plot(filename,year,dvp_flag):
    df = pd.read_csv(filename,low_memory = False)
    title_add = ""
    if dvp_flag:
        title_add = 'DVP ' + str(year)
    else:
        tittle_add = 'Cash Contributions ' +str(year)
    # ethnicity plot
    ethn_counts = df['est_ethnicity'].value_counts()
    ethn_plot = ethn_counts.plot(kind="bar")
    ethn_plot.set_title('Estimated Ethnicity, ' + str(year))
    plt.show()

    # age plot
    age_counts = df['age_bucket'].value_counts()
    age_plot = age_counts.plot(kind="bar")
    age_plot.set_title('Voucher User Age, ' + str(year))
    plt.show()

    # census tract bucket
    income_counts = df['income_bucket'].value_counts()
    income_plot = income_counts.plot(kind="bar")
    income_plot.set_title('Voucher User Census Tract Income Quintile, ' + str(year))
    plt.show()

    # gender
    gender_counts = df['gender'].value_counts()
    gender_plot = gender_counts.plot(kind="bar")
    gender_plot.set_title('Voucher User Census Tract Income Quintile, ' + str(year))
    plt.show()
    
if __name__ == '__main__':
    vouchers_2017 = 'results/2017_vouchers_voter_file_all_cols.csv'
    vouchers_2019 = 'results/2019_vouchers_voter_file_all_cols.csv'
    plot(vouchers_2019,2019,True)
    plot(vouchers_2017,2017,True)

    cash_2017 = 'results/2017_cash_ethnicity_merged_geocoded.csv"
    cash_2019 = "results/2019_cash_ethnicity_merged_geocoded.csv"
    plot(cash_2019,2019,False)
    plot(cash_2017,2017,False)
