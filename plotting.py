import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

def plot(filename,year,dvp_flag):
    df = pd.read_csv(filename,low_memory = False)
    title_add = ""
    if dvp_flag:
        title_add = 'DVP ' + str(year)
    else:
        title_add = 'Cash Contributions ' +str(year)

    # ethnicity plot
    ethn_counts = df['est_ethnicity'].value_counts()
    ethn_plot = ethn_counts.plot(kind="bar")
    ethn_plot.set_title('Estimated Ethnicity, ' + title_add)
    for i in ethn_plot.patches:
        ethn_plot.text(i.get_x() + i.get_width()/2, i.get_height()+i.get_height()/100, str(i.get_height()), horizontalalignment='center', fontsize=10,color='dimgrey')
    plt.show()

    # age plot
    age_counts = df['age_bucket'].value_counts()
    age_counts = age_counts.reindex(index = [1., 2, 3,4])
    age_counts = age_counts.rename(index={1: '18-29 years', 2: '30-44 years old',3:'45-59 years old',4:'60+ years'})
    age_plot = age_counts.plot(kind="bar")
    for i in age_plot.patches:
        age_plot.text(i.get_x() + i.get_width()/2, i.get_height()+i.get_height()/100, str(i.get_height()), horizontalalignment='center', fontsize=10,color='dimgrey')
    age_plot.set_title('Voucher User Age, ' + title_add)
    plt.show()

    # census tract bucket
    quintile_order = ["bottom", "fourth", "middle","second","top"]
    income_counts = df['income_quintile'].value_counts()
    income_counts = income_counts.reindex(index = ["bottom", "fourth", "middle","second","top"])
    income_plot = income_counts.plot(kind="bar")
    for i in income_plot.patches:
        income_plot.text(i.get_x() + i.get_width()/2, i.get_height()+i.get_height()/100, str(i.get_height()), horizontalalignment='center', fontsize=10,color='dimgrey')
    income_plot.set_title('Voucher User Census Tract Income Quintile, ' + title_add)
    plt.show()


    # gender
    gender_counts = df['Gender'].value_counts()
    gender_plot = gender_counts.plot(kind="bar")
    for i in gender_plot.patches:
        gender_plot.text(i.get_x() + i.get_width()/2, i.get_height()+i.get_height()/100, str(i.get_height()), horizontalalignment='center', fontsize=10,color='dimgrey')
    gender_plot.set_title('Voucher User Census Tract Gender, ' + title_add)
    plt.show()
    
if __name__ == '__main__':
    vouchers_2017 = 'results/2017_vouchers_voter_file_all_cols.csv'
    vouchers_2019 = 'results/2019_vouchers_voter_file_all_cols.csv'
    plot(vouchers_2019,2019,True)
    plot(vouchers_2017,2017,True)

    cash_2017 = "results/2017_cash_all_cols.csv"
    cash_2019 = "results/2019_cash_all_cols.csv"
    # plot(cash_2019,2019,False)
    # plot(cash_2017,2017,False)
