"""
A script for analyzing data to find out which country has
most tourists per capita.
"""

import pandas as pd
import matplotlib.pyplot as plt

# Read data from xls files
df_pop = pd.read_excel('population.xls', skiprows=3 )
df_tourists = pd.read_excel('number_of_arrivals.xls', skiprows=3)

# Delete unnecessary columns
df_tourists = df_tourists.iloc[:,[0,1,-2]]
df_pop = df_pop.iloc[:,[0,1,-2]]

# Rename columns
df_tourists.rename(columns={'2018': 'tourists_2018'}, inplace=True)
df_pop.rename(columns={'2018': 'pop_2018'}, inplace=True)

# Merge dataframes
df_tourists = pd.merge(df_tourists, df_pop)

# Drop rows
df_tourists = df_tourists.dropna()

''' Get rid of rows with aggregate country data '''

# Read country metadata from tourist xls file
df_tourist_meta = pd.read_excel('number_of_arrivals.xls', sheet_name = 'Metadata - Countries')

# Drop rows that are empty in 'Region' column
df_tourist_meta = df_tourist_meta.dropna(subset=['Region'])

# Delete all columns except 'Country Code'
df_tourist_meta = df_tourist_meta['Country Code']

# Inner merge to eliminate unnecessary country codes
df_tourists = df_tourists.merge(df_tourist_meta, on='Country Code', how='inner')

# Add column
df_tourists['tourists_per_capita'] = df_tourists['tourists_2018']/df_tourists['pop_2018']

# Sort dataframe
df_tourists = df_tourists.sort_values(by=['tourists_per_capita'], ascending = False)

''' Plot data '''

# Plot tourist with most tourists per capita
top = df_tourists.iloc[10::-1]
bottom = df_tourists.iloc[:-12  :-1]
new_df = pd.concat([top,bottom])
fig = plt.figure()
ax1 = plt.subplot(211)
ax1.barh(top['Country Name'], top['tourists_per_capita'], color='#77b255')
ax2 = plt.subplot(212)
ax2.barh(bottom['Country Name'], bottom['tourists_per_capita'])
plt.show()