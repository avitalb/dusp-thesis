import pandas as pd 
import matplotlib.pyplot as plt

def plot(filename,year):
    df = pd.read_csv(filename,low_memory = False)

    # ethnicity plot
    ethn_counts = df['est_ethnicity'].value_counts()
    ethn_plot = ethn_counts.plot(kind="bar")
    ethn_plot.set_title('Estimated Ethnicity, DVP ' + str(year))
    plt.show()

    # age plot
    age_counts = df['age_bucket'].value_counts()
    age_plot = age_counts.plot(kind="bar")
    age_plot.set_title('Voucher User Age, DVP ' + str(year))
    plt.show()

    # census tract bucket
    income_counts = df['income_bucket'].value_counts()
    income_plot = income_counts.plot(kind="bar")
    income_plot.set_title('Voucher User Census Tract Income Quintile, DVP ' + str(year))
    plt.show()
    
if __name__ == '__main__':
    # merged_2017 = 'results/2017_vouchers_voter_file_all_cols.csv'
    merged_2019 = 'results/2019_vouchers_voter_file_all_cols.csv'
    plot(merged_2019,2019)
    # plot(merged_2017)

