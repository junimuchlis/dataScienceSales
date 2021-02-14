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
all_data['Order Date']

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

# ADD CITY COLUMN
## let's use .apply()

def get_city(address):
    return address.split(',')[1] 
    #917 1st ST, Dallas, TX 75001->this def will extract 2nd index comma from beginning i.e Dallas
    #index in python start from zero

def get_state(address):
    return address.split(',')[2].split(' ')[1]
    # 917 1st ST, Dallas, TX 75001->this def will extract 3rd index comma from beginning i.e TX 75001
    # and extract again the "TX 75001" by the second "space" into "TX"

all_data['City'] = all_data['Purchase Address'].apply(lambda x: f"{get_city(x)} ({get_state(x)})")
all_data['City']



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

# What city had the highest number of sales?
result = all_data.groupby('City').sum()
result.sort_values('Sales', ascending=False)

# plot city with highest number of sales 

cities = [city for city, df in all_data.groupby('City')]

plt.bar(cities, result['Sales'])
plt.xticks(cities, rotation='vertical', size=6)
plt.ylabel('Sales in USD (in Million)')
plt.xlabel('City Name')
plt.tight_layout()
plt.show()

#WHAT TIME SHOULD WE DISPLAY ADVERTISEMENTS TO MAXIMIZE 
#LIKELIHOOD OF CUSTOMERS' BUYING PRODUCT?

all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])
all_data['Order Date']

## add hour and minute column
all_data['Hour'] = all_data['Order Date'].dt.hour
all_data['Minute'] = all_data['Order Date'].dt.minute
all_data[['Hour', 'Minute']].head()

##what time should we display advertisements 
hours = [hour for hour, df in all_data.groupby('Hour')]
plt.plot(hours, all_data.groupby(['Hour']).count())
plt.xticks(hours)
plt.xlabel('Hour')
plt.ylabel('Number of order')
plt.grid()
plt.show()

# WHAT PRODUCTS ARE MOST OFTEN SOLD TOGETHER
df = all_data[all_data['Order ID'].duplicated(keep=False)]
df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df.head()





