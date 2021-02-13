# BETTER RUN IN SPYDER AS MAY EXECUTE BLOCK PER BLOCK
import pandas as pd
import os
import matplotlib.pyplot as plt

# Task 1: Merge the 12 months of sales data into a single CSV
df = pd.read_csv("Sales_Data/Sales_April_2019.csv")
df.head()
df.shape
    #read multiple csv files in directory
files = [file for file in os.listdir('Sales_Data')]
"""
for file in files:
    print(file) #print list of files available

"""
# concate all csv into 1 csv

all_months_data = pd.DataFrame() #1. create an empty dataframe called all_months_data

#iterate and read all csv files
for file in files:
    df = pd.read_csv("Sales_Data/"+file)
    all_months_data = pd.concat([all_months_data,df])

all_months_data.head()
all_months_data.shape
all_months_data.to_csv("Sales_Data/all_data_concat2.csv", index=False)

#pull new dataframe from concat csv
all_data = pd.read_csv("Sales_Data/all_data_concat2.csv")
all_data.shape

#show all columns
list(all_data)
# 'Order ID',  'Product',  'Quantity Ordered', 'Price Each', 'Order Date', 'Purchase Address']

#CLEAN UP DATA
## find Nan
#### find nan if any
check_nanIfAny = all_data.isnull().values.any() #TRUE, yes THERE ARE Some

### check all/sum Nan values
countAllNan = all_data.isnull().sum().sum()
#### check Nan per column
countNanPerColumn = all_data.isnull().sum()

### drop na values
all_data = all_data.dropna(how='all')
all_data.head()
all_data.shape

### recheck NAN Values
recheckNan = all_data.isnull().values.any() #FALSE, yes THERE ARE NOT LEFT

#ValueError: invalid literal for int() with base 10: 'Or'
#find 'Or' delete it
all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']

# convert columns to the correct type
all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])



#AUGMENT DATA WITH ADDITIONAL COLUMNS
##Task 2: Add Month column
all_data.shape
#create columns 'Month' and put 2 initial string from column 'Order Date'
all_data['Month'] = all_data['Order Date'].str[0:2] 
#check data just created from particular column
all_data['Month']
all_data.shape
#convert format string into integer
all_data['Month'] = all_data['Month'].astype('int32')

# ADD SALES COLUMN
list(all_data)
"""
'Order ID', 'Product', 'Quantity Ordered',
 'Price Each', 'Order Date', 'Purchase Address', 'Month'
"""
all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']
all_data['Sales']



#What was the best month for sales? How much was earned that month?
sum1 = all_data.groupby('Month').sum()
sum1.sort_values('Sales', ascending=False)

#plot sales with matplotlib
months = range(1,13)
plt.bar(months, sum1['Sales'])
plt.xticks(months)
plt.ylabel('Sales in USD (value in Million)')
plt.xlabel('Month Number')
plt.show()







