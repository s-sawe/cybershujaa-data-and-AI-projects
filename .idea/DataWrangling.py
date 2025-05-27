import pandas as pd

#Import the Data to a Pandas DataFrame
df = pd.read_csv('C:/Users/SJSawe/Downloads/archive/cybershujaa/netflix_titles.csv')

# 1. DISCOVERY
#Data overview
df.info()

#Number of rows and columns
print("Shape of the dataset (R x C):", df.shape)

#List of all column names
print("Columns in the dataset:\n", df.columns.tolist())

#Data type of each column
print("Data types:\n", df.dtypes)

# Group and Count of missing (null) values in each column
print("Missing values per column:\n", df.isnull().sum())

# Group and Count of duplicate rows
print("Number of duplicate rows:", df.duplicated().sum())

# 2. STRUCTURING
# Convert 'date_added' to datetime
df['date_added'] = pd.to_datetime(df['date_added'],format='mixed')

# Separate 'duration' into numeric value and unit (e.g., '90 min' → 90, 'min')
df[['duration_value', 'duration_unit']] = df['duration'].str.extract(r'(\d+)\s*(\w+)')

# Convert duration_value to numeric
df['duration_value'] = pd.to_numeric(df['duration_value'])

# View Resulting columns
print(df[['duration_value', 'duration_unit']])


# 3. CLEANING
# Check for duplicate rows
print("Duplicate rows before:", df.duplicated().sum())

# Drop duplicate rows if any
df = df.drop_duplicates()

# Drop description column because it will not be used
df = df.drop(columns=['description'])

# Impute Director values by using relationship between cast and director

# List of Director-Cast pairs and the number of times they appear
df['dir_cast'] = df['director'] + '---' + df['cast']
counts = df['dir_cast'].value_counts() #counts unique values
filtered_counts = counts[counts >= 3] #checks if repeated 3 or more times
filtered_values = filtered_counts.index #gets the values i.e. names
lst_dir_cast = list(filtered_values) #convert to list
dict_direcast = dict()
for i in lst_dir_cast :
     director, cast = i.split('---')
     dict_direcast[director]=cast
for i in range(len(dict_direcast)): 
    df.loc[(df['director'].isna()) & (df['cast'] == list(dict_direcast.items())[i][1]),'director'] = list(dict_direcast.items())[i][0]

# Assign Not Given to all other director fields
df.loc[df['director'].isna(),'director'] = 'Not Given'

#Use directors to fill missing countries
directors = df['director']
countries = df['country']

#pair each director with their country use zip() to get an iterator of tuples
pairs = zip(directors, countries)

# Convert the list of tuples into a dictionary
dir_cntry = dict(list(pairs))

# Director matched to Country values used to fill in null country values
for i in range(len(dir_cntry)):    
    df.loc[(df['country'].isna()) & (df['director'] == list(dir_cntry.items())[i][0]), 'country'] = list(dir_cntry.items())[i][1]

# Assign Not Given to all other country fields
df.loc[df['country'].isna(),'country'] = 'Not Given'

# Assign Not Given to all other fields
df.loc[df['cast'].isna(),'cast'] = 'Not Given'

# dropping other row records that are null
df.drop(df[df['date_added'].isna()].index,axis=0,inplace=True)
df.drop(df[df['rating'].isna()].index,axis=0,inplace=True)
df.drop(df[df['duration'].isna()].index,axis=0,inplace=True)

Errors
# check if there are any added_dates that come before release_year
import datetime as dt
sum(df['date_added'].dt.year < df['release_year'])
df.loc[(df['date_added'].dt.year < df['release_year']),['date_added','release_year']]

# sample some of the records and check that they have been accurately replaced
df.iloc[[1551,1696,2920,3168]]

#Confirm that no more release_year inconsistencies
sum(df['date_added'].dt.year < df['release_year'])

# Remove any columns added during wrangling
df.drop(columns=['dir_cast'], inplace=True)

# Sample few rows to check visually
df.sample(5)

# Save as CSV
df.to_csv('C:/Users/SJSawe/Downloads/archive/cybershujaa/cleaned_netflix.csv', index=False)
df.to_csv('/kaggle/working/cleaned_netflix.csv', index=False)