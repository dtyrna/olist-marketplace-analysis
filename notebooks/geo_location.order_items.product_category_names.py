######################################################################################################################################################################
# Jakob's Code
######################################################################################################################################################################

#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#importing libraries


# ## Loading and inspecting the data
# 
# Loading and copying the bronzedataset. Check it with.info() to see missing values and data types. Checking it with the data wrangler.

# In[3]:


df1=pd.read_csv(r"C:\Users\User\Desktop\DSI\Abschlussprojekt\Quelldaten\bronze_olist_geolocation_dataset.csv")
df_geolocation= df1.copy()
df_geolocation.info() 


# ## Find missing values
# 
#  The value_counts matches the rangeindex from above in both cases. There are no missing values. The columns will be converted into strings.

# In[4]:


df_geolocation['geolocation_city'].apply(type).value_counts()
df_geolocation['geolocation_state'].apply(type).value_counts()


# In[5]:


spalten_liste= ['geolocation_city','geolocation_state']
df_geolocation[spalten_liste]=df_geolocation[spalten_liste].astype("string")
df_geolocation.info()


# ## Dropping of unwanted columns 
# 
# The columns of longitute and latitute will be removed. They don't give us a gain of information on this dataset, since it doesn't clarify more about the sellers. Every row has different measures and the table would become to large and to fine. So we decided to drop those columns and keep the zip-code of the cities as well as the state as category.

# In[14]:


df_geolocation = df_geolocation.drop(columns=['geolocation_lat', 'geolocation_lng'])


# ## Data Cleaning
# 
# It starts with checking the state. Is has to be two charakters long in brazil. After that it will checked if there are special characters in the column. The will be converted into snake case and whitespaces will be removed. 
# 

# In[15]:


state_lengths = df_geolocation['geolocation_state'].str.len()
state_lengths_count = state_lengths.value_counts()
print(f"Distribution of lengths: {state_lengths_count}")



broken_states = df_geolocation[state_lengths != 2]
if not broken_states.empty:
    print(f" The following lines are incorrect: {broken_states}")
else:
    print(f"There are no data errors!")


# In[24]:


df_geolocation['geolocation_state'] = df_geolocation['geolocation_state'].str.strip().str.lower()
string_elements="".join(df_geolocation['geolocation_state'])
unique_strings=sorted(list(set(string_elements)))
print(f" The following characters are in the column {unique_strings}")


# ## Data Cleaning
# 
#  The portuguese letters and special characters will be removed, as well as the white spaces.
#  The dictonary corrects the most common mistakes. 

# In[41]:


string_elements="".join(df_geolocation['geolocation_city'])
unique_strings=sorted(list(set(string_elements)))
print(unique_strings)

replacements={'â': 'a', 'í': 'i', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ü': 'u', '´': '', '`': '', 'º': '' }
df_geolocation['geolocation_city'] = df_geolocation['geolocation_city'].str.lower().str.strip().replace(replacements, regex=True)
df_geolocation['geolocation_city'] = df_geolocation['geolocation_city'].str.replace(r'[^a-z\s\-]', '', regex=True)
df_geolocation['geolocation_city'] = df_geolocation['geolocation_city'].str.strip() 


city_names = df_geolocation[df_geolocation['geolocation_city'].str.contains(' ', na=False)]
clean_city_names=city_names['geolocation_city'].value_counts()
print(clean_city_names)


# A last check on whitespaces and unique strings as well as correcting spelling mistakes in the city column.

# In[42]:


orthography={'so paulo': 'sao paulo', 'jos bonifcio': 'jose bonifacio','jose bonifactio':'jose bonifacio' ,'sopaulo':'sao paulo','sp':'sao paulo','poa':'porto alegre', 'po':'port alegre','mogidascruzes':'mogi das cruzes','biritiba-mirim':'biritiba mirim','santo andr':'santo andre'}
df_geolocation['geolocation_city']=df_geolocation['geolocation_city'].replace(orthography,regex=True) 


print(city_names['geolocation_city'])

whitespaces = df_geolocation[df_geolocation['geolocation_city'].str.startswith(' ') | df_geolocation['geolocation_city'].str.endswith(' ')]

print(whitespaces)


string_elements="".join(df_geolocation['geolocation_city'])
unique_strings=sorted(list(set(string_elements)))
print(unique_strings)


# ## Data Validating
# 
#  Unusal and usual combinations of citys and states will be detected and corrected.

# In[20]:


combinations= df_geolocation.groupby(['geolocation_state','geolocation_city'])
top_combinations=combinations.head(20)
unusual_combinations=combinations.tail(20)
print(f"The most common combinations are {top_combinations}")
print(f"Unusual combinations are {unusual_combinations}")


# ## Correcting incorrect distributions and rechecking them

# In[65]:


grouped_combinations = df_geolocation.groupby(['geolocation_city', 'geolocation_state']).size().reset_index(name='count')
sorted_combinations = grouped_combinations.sort_values(['geolocation_city', 'count'], ascending=[True, False])


correct_pairs = sorted_combinations.drop_duplicates(subset=['geolocation_city'])

correct_combinations = dict(zip(correct_pairs['geolocation_city'], correct_pairs['geolocation_state']))


df_geolocation['geolocation_state'] = df_geolocation['geolocation_city'].map(correct_combinations)

df_geolocation.info()
df_geolocation['geolocation_state']=df_geolocation['geolocation_state'].astype('string')
df_geolocation.info()


# In[28]:


combinations= df_geolocation.groupby(['geolocation_state','geolocation_city'])
top_combinations=combinations.head(20)
unusual_combinations=combinations.tail(20)
print(f"The most common combinations are {top_combinations}")
print(f"Unusual combinations are {unusual_combinations}")


# ## Removing Duplicates

# In[32]:


df_geolocation = df_geolocation.drop_duplicates() # removing duplicates
df_geolocation


# ## Converting the zipcode and bring it into 5 figure format
# 
#  Converting zipcode into a string format. It is easier to work with, since a zipcode won't be used in metric operations.

# In[38]:


df_geolocation["geolocation_zip_code_prefix"]=df_geolocation["geolocation_zip_code_prefix"].astype(str).str.zfill(5)

df_geolocation["geolocation_zip_code_prefix"]=df_geolocation["geolocation_zip_code_prefix"].astype("string")
zip_length= df_geolocation["geolocation_zip_code_prefix"].str.len()
distribution_zip=zip_length.value_counts()
correct_length=distribution_zip.get(5,0)
print(f"There are {correct_length} with 5 figure length")

if correct_length == len(df_geolocation):
    print("Every zip-code has the correct length.")
else:
    incorrect_rows = len(df_geolocation) - correct_length
    print(f"There are {incorrect_rows} errors in the column.")


# ## Setting a index as surrogate key 
# 
# Max length of the strings int he column will be determined and an index will be set. Unusual names will be dropped, since there are no cities in brazil with more than 32 characters.

# In[ ]:


city_counts = df_geolocation['geolocation_city'].value_counts()


valid_cities = city_counts[city_counts >= 2].index


df_geolocation = df_geolocation[df_geolocation['geolocation_city'].isin(valid_cities)]
largest_city=df_geolocation['geolocation_city'].str.len().max()
print(f"max characters of the city column: {largest_city}")

df_geolocation.info()


# In[ ]:


df_geolocation=df_geolocation.reset_index(drop=True)#
df_geolocation['id_geolocation']=df_geolocation.index+1
df_geolocation=df_geolocation.set_index('id_geolocation')
display(df_geolocation)
df_geolocation.to_csv('silver.geolocation.csv',index=False,encoding='utf-8')
df_geolocation.info()


# ## Loading and inspecting the data

# In[44]:


df2=pd.read_csv(r"C:\Users\User\Desktop\DSI\Abschlussprojekt\Quelldaten\bronze_product_category_name_translation.csv")
df_product_name_translation=df2.copy()
df_product_name_translation.info()



# # Transform the data
# 
# Transform datatype object into stringtype.

# In[ ]:


df_product_name_translation['product_category_name'].apply(type).value_counts()
df_product_name_translation['product_category_name_english'].apply(type).value_counts()

spalten_liste= ['product_category_name','product_category_name_english']
df_product_name_translation=df_product_name_translation[spalten_liste].astype("string")
df_product_name_translation.info()


# # Data Cleaning
# 
# Removing whitespaces and transform it into snake case strings. Checking the strings for special charakters and removing duplicates.

# In[15]:


df_product_name_translation['product_category_name'] = df_product_name_translation['product_category_name'].str.strip().str.lower()
df_product_name_translation['product_category_name_english'] = df_product_name_translation['product_category_name_english'].str.strip().str.lower()

string_elements="".join(df_product_name_translation['product_category_name'])
unique_strings=sorted(list(set(string_elements)))
print(unique_strings)

string_elements="".join(df_product_name_translation['product_category_name_english'])
unique_strings=sorted(list(set(string_elements)))
print(unique_strings)
df_product_name_translation.drop_duplicates()


# ## Index as surrogate key 
# 
# The index will be the surrogate key. The max. string length will be estimated to create a clean and fast database.

# In[68]:


df_product_name_translation=df_product_name_translation.reset_index(drop=True)
df_product_name_translation['id_product_name_translation']=df_product_name_translation.index+1
df_product_name_translation=df_product_name_translation.set_index('id_product_name_translation')

max_length_portuguese=df_product_name_translation['product_category_name'].str.len().max()
max_length_english=df_product_name_translation['product_category_name'].str.len().max()

print(f"The max length of characters of the portugese column is {max_length_portuguese}.")
print(f"The max length of characters of the english column is {max_length_english}.")

df_product_name_translation.info()

display(df_product_name_translation)
df_product_name_translation.to_csv('silver.product_category_name_translation.csv',index=False,encoding='utf-8')


# # Inspecting the order items table
# 
# This table shows the order amount.

# In[70]:


df3=pd.read_csv(r"C:\Users\User\Desktop\DSI\Abschlussprojekt\Quelldaten\bronze_olist_order_items_dataset.csv")
df_order_items=df3.copy()
df_order_items.info()
df_order_items


# ## Transforming the data
# 
# First the object will be inspected and see if it matches the index. Secondly, it is assessed if there are different datatypes in the object.

# In[79]:


check_order=df_order_items['order_id'].apply(type).value_counts()
check_product=df_order_items['product_id'].apply(type).value_counts()
check_seller=df_order_items['seller_id'].apply(type).value_counts()
check_date=df_order_items['shipping_limit_date'].apply(type).value_counts()

print(check_date)
print(check_order)
print(check_product)
print(check_date)


# There are no mixed types in the object, so the columns will be transferred into strings and the datetime64 in datetimeformat. There are no missing values sinced the count matches the rangeIndex.

# In[101]:


df_order_items['shipping_limit_date'].apply(type).value_counts()
df_order_items['shipping_limit_date']=df_order_items['shipping_limit_date'].astype('datetime64[ns]')


df_order_items['seller_id'].apply(type).value_counts()
df_order_items['seller_id']=df_order_items['seller_id'].astype('string')


df_order_items['order_id'].apply(type).value_counts()
df_order_items['order_id']=df_order_items['order_id'].astype('string')


df_order_items['product_id'].apply(type).value_counts()
df_order_items['product_id']=df_order_items['product_id'].astype('string')
df_order_items.info()


# ## Data Validation
# 
# The colums will be checked in terms of unusal long string, special characters, unreasonable values or null values. There none null values detected

# In[102]:


zero_values_order_value=df_order_items['order_item_id'].isna().sum()
print(f"There are {zero_values_order_value} null values in column order item id (amount)")
zero_values_order_price=df_order_items['price'].isna().sum()
print(f"There are {zero_values_order_price} null values in thecolumn price.")
zero_values_order_freight_value=df_order_items['freight_value'].isna().sum()
print(f"There are {zero_values_order_freight_value} null values in column freight value ")


# In[103]:


df_order_items['order_id'] = df_order_items['order_id'].str.strip().str.lower()

df_order_items['product_id'] = df_order_items['product_id'].str.strip().str.lower()
df_order_items['seller_id'] = df_order_items['seller_id'].str.strip().str.lower()

string_elements="".join(df_order_items['order_id'])
unique_strings=sorted(list(set(string_elements)))
print(unique_strings)

string_elements="".join(df_order_items['product_id'])
unique_strings=sorted(list(set(string_elements)))
print(unique_strings)

string_elements="".join(df_order_items['seller_id'])
unique_strings=sorted(list(set(string_elements)))
print(unique_strings)



# # Data Validation

# In[104]:


min_qty = df_order_items['order_item_id'].min()
max_qty = df_order_items['order_item_id'].max()

print(f"Order quantity minimum: {min_qty} and maximum: {max_qty}")




# Checking for wrong values. Since the divison operation itself can produce figures with more than 2 figures after the ., it will converted into strings to assure the correct format.

# In[105]:


min_freight = df_order_items['freight_value'].min()
max_freight = df_order_items['freight_value'].max()

print(f"Shipping cost minimum: {min_freight} and maximum: {max_freight}")

wrong_floats_freight = ((df_order_items['price'] * 100) % 1 != 0).sum()

print(f"Prices with to many figures after the .: {wrong_floats_freight} rows")

freight_as_string = df_order_items['price'].round(2).astype(str)
freight_check = freight_as_string.str.split('.').str[1].str.len()

print(f" Max. number of figures after the .:{freight_check.max()}")


# In[ ]:


min_price = df_order_items['price'].min()
max_price = df_order_items['price'].max()

print(f"Order value  minimum: {min_price} and maximum: {max_price}")

wrong_floats = ((df_order_items['price'] * 100) % 1 != 0).sum()

print(f"Prices with to many figures after the .: {wrong_floats} rows")
df_order_items['price'] = df_order_items['price'].round(2)

float_check = ((df_order_items['price'] * 100) % 1 != 0).sum()

print(f"Prices with to many figures after the .: {float_check} rows")


price_as_string = df_order_items['price'].round(2).astype(str)
float_check = price_as_string.str.split('.').str[1].str.len()


print(f"Figures after the point : {float_check.max()}")


# ## Checking the key columns
# 
# All keys have length of 32 characters in 112650 rows. There are no unusual patterns.

# In[112]:


order_id_len = df_order_items['order_id'].str.len().value_counts()
product_id_len = df_order_items['product_id'].str.len().value_counts()
seller_id_len = df_order_items['seller_id'].str.len().value_counts()


print(f"The len of the {order_id_len}")


print(f"The len of the {product_id_len}")


print(f"The len of the {seller_id_len}")



# ## Setting an surrogate key

# In[ ]:


df_order_items=df_order_items.reset_index(drop=True)
df_order_items['id_olist_order_items']=df_order_items.index+1
df_order_items=df_order_items.set_index('id_olist_order_items')
df_order_items.drop_duplicates()


# ## Checking the amount and the price with basic statistics
# 
# The statistics show,  that chiefly small orders are put. The standart deviation is with 0.7 low. There are a couple of very large orders. The price column reflects this. This can be senn looking at the median. Since the price is a larger figure, the other figures rise. The std is larger than the mean. There is at the max larger orders.

# In[ ]:


df_order_items.describe()


# ## Reorder the columns the make the table clearly unstandable

# In[ ]:


reorder_columns= ['order_id','product_id','seller_id','shipping_limit_date','order_item_id','price','freight_value']
df_order_items=df_order_items[reorder_columns]
df_order_items
display(df_order_items)
#df_order_items.to_csv('silver.olist_order_items_dataset.csv',index=False,encoding='utf-8')

