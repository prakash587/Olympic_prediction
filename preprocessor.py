import pandas as pd



def preprocess(df, country_df):

    #filtering for summer olympics
    df= df[df['Season']=='Summer']

    #merge with country df
    df= df.merge(country_df, how='left', on='NOC')

    #DROPPING DUPICATES
    df.drop_duplicates(inplace=True)

    #one hot encoding medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    return df