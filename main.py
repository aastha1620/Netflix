#Importing all the necessary python libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Checking on the uploaded dataset.
df= pd.read_csv('mymoviedb.csv',lineterminator = '\n')
df.head()

#Cleaning and preparing the dataset
df.duplicated().sum()
df.describe()

#Exploration Summary

1) We have a dataframe consisting of 9827 rows and 9 columns.
2) Our dataset looks a bit tidy with no NaNs nor duplicated values.
3) Release_Date column needs to be casted into datetime and to extract only the year value.
4) Overview, Original_Language and Poster-Url wouldn't be so useful during analysis, so we'll drop them.
5) There is noticeable outliers in the Popularity column.
6) Vote_Average better be categorized for proper analysis.
7) Genre column has comma-separated values and white spaces that need to be handled and casted into a category.


# Release_Date column needs to be casted into datetime and to extract only the year value.
df['Release_Date'] = pd.to_datetime(df['Release_Date'])
print(df['Release_Date'].dtypes)

df['Release_Date'] = df['Release_Date'].dt.year
df['Release_Date'].dtypes
df.head()

#Dropping the unecessary Columns
cols = ['Overview','Original_Language','Poster_Url']
df.drop(cols,axis=1,inplace= True)
df.head()

#Categorizing Vote_Average column: We would cut the 'Vote_Average' values and make 4 categories: 'popular', 'average', 'below_avg', 'not_popular' to describe it more using 'categorize_col()' function provided above.
def categorize_col(df, col, labels):
# Created function
    edges = [
        df[col].describe()['min'],
        df[col].describe()['25%'],
        df[col].describe()['50%'],
        df[col].describe()['75%'],
        df[col].describe()['max']
    ]
    
    df[col] = pd.cut(df[col], edges, labels=labels, duplicates='drop')
    return df

# Define the labels
labels = ['not_popular', 'below_avg', 'average', 'popular']

# Call the function
df = categorize_col(df, 'Vote_Average', labels)

# Check unique categories
print(df['Vote_Average'].unique())
df.head()

df['Vote_Average'].value_counts()

# to drop all the null data
df.dropna(inplace = True)
df.isna().sum()

#We'd split the genres into a list and then explode our dataframe to have only one genre per row for each movie
df['Genre'] = df['Genre'].str.split(', ')

df = df.explode('Genre').reset_index(drop=True)
df.head()

#casting column into category

df['Genre'] = df['Genre'].astype('category')

df['Genre'].dtypes
df.info()
df.nunique()

# Data visualization
sns.set_style('whitegrid')

#what is the most frequent genre of movies released on netflix?
df['Genre'].describe()
sns.catplot(y = 'Genre', data = df, kind = 'count',
            order = df['Genre'].value_counts().index,
            color = '#4287f5')
plt.title('Genre column distribution')
plt.show()


#Which has highest votes in vote avg column?
sns.catplot(y = 'Vote_Average', data = df, kind = 'count',
            order = df['Vote_Average'].value_counts().index,
            color = '#4287f5')
plt.title('Votes Distribution')
plt.show()

#What movie got the highest popularity ? what's its genre?
df[df['Popularity'] == df['Popularity'].max()]

#What movie got lowest popularity?
df[df['Popularity'] == df['Popularity'].min()]

#Which year has the most filmmed movies?
df['Release_Date'].hist()
plt.title('Release date column distribution')
plt.show()

#summary
# Q1: What is the most frequent genre in the dataset?
# Drama genre is the most frequent genre in our dataset and has appeared more than 14% of the times among 19 other genres.

# Q2: What genres has highest votes?
# We have 25.5% of our dataset with popular vote (6520 rows). Drama again gets the highest popularity among fans by being having more than 18.5% movies.

# Q3: What movie got the highest popularity? What's its genre?
# Spider-Man: No Way Home has the highest popularity rate in our dataset and it has genres of Action, Adventure and Science Fiction.

# Q4: What movie got the lowest popularity? What's its genre?
# The United States, 'thread' has the highest lowest rate in our dataset and it has genres of music, drama, 'war', 'sci-fi' and history.

# Q5: Which year has the most filmed movies?
# Year 2020 has the highest filming rate in our dataset.

