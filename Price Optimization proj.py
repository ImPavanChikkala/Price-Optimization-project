import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('D:/Competition_Data.csv')
print(data.head())
print(data.tail())
print(data.info())


#comparint our price and competiton price
plt.figure(figsize = (12,6))

plt.subplot(1,2,1)
plt.hist(data['Price'],bins = 30,alpha = 0.7,label = 'your store')
plt.xlabel('price')
plt.ylabel('Frequency')
plt.legend()
plt.title("Price Distribution -Your store")

plt.subplot(1,2,2)
plt.hist(data['Competition_Price'],bins = 30,alpha=0.7,color ='orange',label = 'competition')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.legend()
plt.title('Price Distribution-Competition')

plt.tight_layout()
plt.show()

# let’s compare the relationship between price and sales

plt.figure(figsize = (12,6))

plt.subplot(1,2,1)
plt.scatter(data['Price'],data['Sales_Amount'],alpha = 0.9,label = 'your store')
plt.xlabel('price')
plt.ylabel('Sales Amount')
plt.legend()
plt.title("Your Price vs sales Amount")

plt.subplot(1,2,2)
plt.scatter(data['Competition_Price'],data['Sales_Amount'],alpha=0.1,color ='orange',label = 'competition')
plt.xlabel('Competition Price')
plt.ylabel('Sales amount')
plt.title('Competition Price vs Sales Amount')

plt.tight_layout()
plt.show()

#let’s compare the price changes over time:
data.rename(columns={"Fiscal_Week_ID":"Week_num"},inplace=True)
data['Week_num']=pd.to_datetime(data['Week_num']+'-1',format='%Y-%U-%w')
#print(data['Week_num'])
weekly_prices = data.groupby('Week_num').agg({
    'Price':'mean',#key = column name,value = funct(mean is a function)
    'Competition_Price':'mean'
}).reset_index()
plt.figure(figsize=(12,6))

plt.plot(weekly_prices['Week_num'],weekly_prices['Price'],label='Our store',marker='o')
plt.plot(weekly_prices['Week_num'],weekly_prices['Competition_Price'],label='Competiton',marker='o',color = 'orange')
plt.xlabel('Week num')
plt.ylabel('Average_price')
plt.title('Price Changes over time')
plt.legend()
plt.grid(True)
plt.show()
print(data.describe())
#group by method averages similars values and make a group
#To apply more agg function we need to use dict in agg method

#let’s analyze how changes in prices affect the change in quantity sold
#Here’s the formula used to calculate price elasticity:
#Ed = % change in quantity demanded / % change in price

data['Price_change']=data['Price'].pct_change()
data['qty_change']=data['Item_Quantity'].pct_change()
#print(data['Price_change'].head())
#print(data['qty_change'].head())

data['elasticity']=data['qty_change']/data['Price_change']
#print(data['elasticity'])
data.replace([float('inf'),-float('inf')],float('nan'),inplace=True)
#inf means infinite and minus float of ins represents minus infinite
print(data.shape)
data.dropna(subset=['elasticity'],inplace=True)
print(data.shape)
#print(data.describe())

plt.figure(figsize=(12,6))
plt.plot(data['Week_num'],data['elasticity'], marker='o', linestyle='-', color='purple')
plt.axhline(0, color='grey', linewidth=0.8)#Horizantal line
plt.xlabel('week num')
plt.ylabel('Price Elasticity of demand')#elasticity=qty change/price change
plt.title('Price Elasticity of demand over time')
plt.grid(True)
plt.show()

#During high elasticity some weeks sales are high and some weeks sales are low
#elasticity doesnt depends on price now we need find factors other than price

#let’s calculate and compare the total sales amounts for our store and the competition:
total_sales_your_store = data['Sales_Amount'].sum()
total_sales_competition = (data['Competition_Price']*data['Item_Quantity']).sum()
#competiton doesnt have sales amunt thats why we multiplied price *item qty
total_qty_your_store = data['Item_Quantity'].sum()
total_qty_competition = data['Item_Quantity'].sum()
summary = pd.DataFrame({
    'metric':['Total sales amount','Total Quantity sold'],
    'your store':[total_sales_your_store,total_qty_your_store],
    'competition':[total_sales_competition,total_qty_competition]
})
print(summary)

#we’ll analyze how the sales amounts vary across different price brackets to identify if there are specific price ranges where the competition outperforms our store:
# define price brackets
bins = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
labels = ['0-50', '51-100', '101-150', '151-200', '201-250', '251-300', '301-350', '351-400', '401-450', '451-500']

# create price brackets for both your store and competition
data['price_bracket'] = pd.cut(data['Price'], bins=bins, labels=labels, right=False)
data['competition_price_bracket'] = pd.cut(data['Competition_Price'], bins=bins, labels=labels, right=False)

# calculate sales amount by price bracket for your store
sales_by_bracket_your_store = data.groupby('price_bracket')['Sales_Amount'].sum().reset_index()
sales_by_bracket_your_store.columns = ['Price Bracket', 'Your Store Sales Amount']

# calculate sales amount by price bracket for competition
data['competition_sales_amt'] = data['Competition_Price'] * data['Item_Quantity']
sales_by_bracket_competition = data.groupby('competition_price_bracket')['competition_sales_amt'].sum().reset_index()
sales_by_bracket_competition.columns = ['Price Bracket', 'Competition Sales Amount']

sales_by_bracket = pd.merge(sales_by_bracket_your_store, sales_by_bracket_competition, on='Price Bracket')

print(sales_by_bracket)

