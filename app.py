import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# Title of the app
st.title('Welcome to Flipkart Data!')

# Read csv
df = pd.read_csv('flipkart_sales.csv')
# st.write(df)

# Filtering the data
st.sidebar.title('Filter data')


# filter by city
st.sidebar.subheader('Filter by City')
selected_city = st.sidebar.selectbox('Select city', df['City'].unique())
st.write(df[df['City'] == selected_city])

st.sidebar.subheader('Filter by Region')
selected_region = st.sidebar.selectbox('Select Region', df['Region'].unique())
st.write(df[df['Region'] == selected_region])


# take input from user
city = st.selectbox('Select City', df['City'].unique())

# Number of orders placed in city
st.write('Number of orders placed in city')
st.write(df[df['City'] == city]['OrderID'].count())

# Total sales in lucknow
st.write('Total sales in city')
sales_count = df[df['City'] == city]['Sales'].sum()
st.write(sales_count)

# Average sales in lucknow
st.write('Total Profits in city')
sales_count = df[df['City'] == city]['Profit'].sum()
st.write(sales_count)


# st.sidebar.subheader('search by product')
# search_product = st.sidebar.text_input('search product')
st.sidebar.subheader('Search Product')
search_product=st.sidebar.text_input('Enter Product Name')
df[df['ProductName'].str.contains(search_product,case=False)]

region_data = df['Region'].value_counts()
st.write(region_data)

fig, ax = plt.subplots()
ax.pie(region_data, labels=region_data.index, autopct='%1.1f%%')
st.pyplot(fig)



st.header('Pie chart for SubCategory:')
sub_category_data = df['SubCategory'].value_counts()
# st.write(sub_category_data)
fig, ax = plt.subplots()
ax.pie(sub_category_data, labels=sub_category_data.index, autopct='%1.1f%%')
ax.legend()
st.pyplot(fig)


st.header('Line chart for profit and sales')
line_data = df.groupby('OrderDate')[['Sales','Profit']].sum()
st.write(line_data)
fig, ax = plt.subplots()
ax.plot(line_data.index, line_data['Sales'], label='Sales')
ax.plot(line_data.index, line_data['Profit'], label='Sales')
ax.legend()
st.pyplot(fig)

# Group by sales and profit
st.write('Group by sales and profit')
res = df.groupby('OrderDate')[['Sales', 'Profit']]
for sales, profit in res:
    st.write(sales)
    st.write(profit)

st.write('Group by sales and profit sum')
res = df.groupby('OrderDate')[['Sales', 'Profit']].agg('sum')
st.write(res)