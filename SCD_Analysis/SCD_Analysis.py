"""
    Strictly Come Dancing results analysis
"""
__author__ = 'adarsh'

import pandas as pd
from bokeh.plotting import figure, output_file, show

SCD_FILE = '../SCD-Results.csv'

def main():
    df = pd.read_csv(SCD_FILE)
    print type(df)

    # ----- boken plot
    x = df['Week'].tolist()
    y = df['Total'].tolist()
    output_file("lines.html", title="line plot example")
    p = figure(title="week num vs score", x_axis_label='x', y_axis_label='y')
    p.line(x, y)
    #show(p)
    # ------ bokeh plot

    # ------  standardize scores across years
    for i in range(0,len(df)):
        for jury in ['Craig','Arlene','Len','Bruno','Alesha','Darcey','Jennifer','Donny']:
            if df[jury][i] == '-':
                df[jury][i] = None
        if df['Total'][i] == '-':
            df['Total'][i] = None

    #Check we have removed all '-'
    assert (len(df['Total'][df['Total'] == '-']) == 0)
    #Noramlized totals in new column.
    df['NormalizedTotal'] = pd.Series([0]*len(df))
    for i in range(0, len(df)):
        num_juries = 0
        for jury in ['Craig','Arlene','Len','Bruno','Alesha','Darcey','Jennifer','Donny']:
            if df[jury][i] is not None:
                num_juries+=1
            #print( num_juries)
        if df['Total'][i] is not None and num_juries >0:
            df['NormalizedTotal'][i] = int(df['Total'][i])* (4/num_juries)


    #Calculate Avg scores by Series and week.
    avg_by_week = df.groupby(['Week'])['NormalizedTotal'].mean()
    avg_by_series = df.groupby(['Series'])['NormalizedTotal'].mean()

    #Normalizing Dance types where we have two dance types
    df['Dance_Type_1'] = df['Dance'].str.split('and').apply(pd.Series)[0].str.strip()
    df['Dance_Type_2'] = df['Dance'].str.split('and').apply(pd.Series)[1].str.strip()

    #ugly hack to remove the difference due to case diff
    df['Dance_Type_1'] = df['Dance_Type_1'].str.replace('waltz', 'Waltz')
    df['Dance_Type_1'] = df['Dance_Type_1'].str.replace('cha', 'Cha')
    #prints out the distinct list of dance types 1.
    df['Dance_Type_1'].unique()

    #stats for noramlized scores for different dance types over the seaasons
    df.groupby([ 'Dance_Type_1', 'Series'])['NormalizedTotal'].mean()

    #count of the different dance types over Series
    df.groupby([ 'Series',])['Dance_Type_1'].value_counts()


















if __name__ == '__main__':
    main()