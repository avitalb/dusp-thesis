import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

def plotting(data1,data2, data1_name, data2_name, xlabel, colors, column, title, figure_num,flag = "", age_special_case = False):
    mpl.style.use("seaborn")
    mpl.rcParams.update({'axes.titlesize': 18, 'font.size':16, 'axes.labelsize': 16})

    df1 = pd.read_csv(data1,low_memory = False)
    df2 = pd.read_csv(data2, low_memory = False)

    data1_counts = df1[column].value_counts().sort_index()
    data2_counts = df2[column].value_counts().sort_index()

    if flag == "income":
        data1_counts = data1_counts.reindex(index = ["bottom", "fourth", "middle","second","top"])
        data2_counts = data2_counts.reindex(index = ["bottom", "fourth", "middle","second","top"])
    elif flag == "age":
        data1_counts = data1_counts.reindex(index = [1, 2, 3,4])
        data1_counts = data1_counts.rename(index={1: '18-29 years', 2: '30-44 years old',3:'45-59 years old',4:'60+ years'})
        data2_counts = data2_counts.reindex(index = [1, 2, 3,4])
        if age_special_case:
            data2_counts[1] = 0
        data2_counts = data2_counts.rename(index={1: '18-29 years', 2: '30-44 years old',3:'45-59 years old',4:'60+ years'})
    labels = data1_counts.index.to_list()

    data1_vals = data1_counts.values
    data2_vals = data2_counts.values

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, data1_vals, width, label=data1_name, color = colors[0])
    rects2 = ax.bar(x + width/2, data2_vals, width, label=data2_name, color = colors[1])

    ax.set_ylabel('# of people')
    ax.set_title(title, wrap = True)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    


    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = int(rect.get_height())
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize = 12)


    autolabel(rects1)
    autolabel(rects2)
    txt = xlabel + "\n\n\nFigure " + str(figure_num)
    ax.set_xlabel(txt)

    fig.tight_layout()

    plt.savefig('graphs/' + title, bbox_inches = "tight")
    plt.show()

if __name__ == '__main__':
    vouchers_2017 = 'results/2017_vouchers_voter_file_all_cols.csv'
    vouchers_2019 = 'results/2019_vouchers_voter_file_all_cols.csv'
    cash_2017 = "results/2017_cash_all_cols.csv"
    cash_2019 = "results/2019_cash_all_cols.csv"



    # voucher age
    plotting(vouchers_2017, vouchers_2019, "Vouchers 2017", "Vouchers 2019", "Aggregated Age",["C1","C2"], 
    "age_bucket", "Voucher Users in 2017 vs 2019: Participants by Aggregated Age", 2, "age", True)
    # cash age
    plotting(cash_2017, cash_2019, "Cash Contributors 2017", "Cash Contributors 2019", "Aggregated Age",["C3","C4"], 
    "age_bucket", "Cash Contributors in 2017 vs 2019: Participants by Aggregated Age", 3, "age")

    # voucher income
    plotting(vouchers_2017, vouchers_2019, "Vouchers 2017", "Vouchers 2019", "Neighborhood Income Quintile",["C1","C2"], 
    "income_quintile", "Voucher Users in 2017 vs 2019: Participants by Census Tract Income Quintile", 4, "income")
    # cash income 
    plotting(cash_2017, cash_2019, "Cash Contributors 2017", "Cash Contributors 2019", "Neighborhood Income Quintile",["C3","C4"], 
    "income_quintile", "Cash Contributors in 2017 vs 2019: Participants by Census Tract Income Quintile", 5,"income")
    
    # voucher ethnicity 
    plotting(vouchers_2017, vouchers_2019, "Vouchers 2017", "Vouchers 2019", "Estimated Ethnicity",["C1","C2"], 
    "est_ethnicity", "Voucher Users in 2017 vs 2019: Participants by Estimated Ethnicity", 6)

    #cash ethnicity
    plotting(cash_2017, cash_2019, "Cash Contributors 2017", "Cash Contributors 2019", "Estimated Ethnicity",["C3","C4"], 
    "est_ethnicity", "Cash Contributors in 2017 vs 2019: Participants by Estimated Ethnicity", 7)

    # voucher gender
    plotting(vouchers_2017, vouchers_2019, "Vouchers 2017", "Vouchers 2019", "Gender",["C1","C2"], 
    "Gender", "Voucher Users in 2017 vs 2019: Participants by Gender", 8)

    # cash gender
    plotting(cash_2017, cash_2019, "Cash Contributors 2017", "Cash Contributors 2019", "Gender",["C3","C4"], 
    "Gender", "Cash Contributors in 2017 vs 2019: Participants by Gender",9)


