# -*- coding: utf-8 -*-
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Collect historical data from NIFTY 50 Index
# This helps in more realistic variations in investment returns

ticker = "^NSEI"
start_date = "2009-12-31"
end_date = "2024-04-07"

data = yf.download(ticker, start=start_date, end=end_date)
data_filled = data.fillna(method='ffill')
print(data_filled)

# Calculate monthly returns
monthly_returns = data_filled['Adj Close'].resample('M').last().pct_change()

# Calculate monthly volatility
monthly_volatility = monthly_returns.std()

# Print the results
print("Monthly Returns:")
print(monthly_returns)
print("Average Monthly Returns:")
print(monthly_returns.mean())
print("\nMonthly Volatility:")
print(monthly_volatility)

# Defining Financial Variables

inflows={'annual_income':600_000,
         'starting_assets':5_00_000}

outflows={'rent': 15000,  
            'credit_card_payment': 5000, 
            'medical_insurance': 1500, 
            'pension_contribution': 2000,  
            'misc': 5000} 

variables={'start_date':"2024-04-08",
           'years':10,
           'tax_on_income':0.25,
           'avg_income_raise':0.05,
           'avg_inflation_rate':0.06,
           'tax_on_investment':0.30,
           'avg_monthly_market_returns':monthly_returns.mean(),
           'avg_monthly_market_volatility':monthly_volatility}

# Initialize lists for storing income and ROI trend over time

income_history = []
ROI_history = [] 

assets_starting_list = [inflows['starting_assets']] 
assets_ending_list = [] 
months = variables['years'] * 12

# Creating a Simulation Loop
## Our monthly assets calculation involves adding the inflows and subtracting 
## the outflows, while also considering any tax deductions or market factors.
 
for month in range(months):
    
    if assets_ending_list: 
        assets_starting_list.append(assets_ending_list[-1])
    
    current_assets=assets_starting_list[-1]
    
    ## The starting assets for each month would be the ending assets from the 
    ## last month
    
    ## First we account for all the expenses and obligations that 
    ## needs to be paid off
    current_assets-=sum(outflows.values())
    
    ## Taking our current assets as the base for investment,
    ## calculate the ROI
    
    market_return=np.random.normal(variables['avg_monthly_market_returns'], 
                                     variables['avg_monthly_market_volatility'],
                                    1)[0]

    investment_return = (current_assets * market_return) * (1 - variables['tax_on_investment'])
  
    ROI_history.append(investment_return)
    current_assets+=investment_return
    
    ## Add in the net income to assets
    
    net_income = (inflows['annual_income'] * 
                   (1 - variables['tax_on_income'])) / 12
    
    current_assets += net_income
   
    
    # Now these assets would remain at the end of the month
    assets_ending = current_assets
    # store ending assets value
    assets_ending_list.append(assets_ending)  
    
    # For every completion of a year
    ## we have to be sure to not add the raise at the starting 
    ## but rather at the completion of each year and also consider 
    ## applying the inflation rate each consecutive year
    
    if (month % 12 == 0):
            inflows['annual_income'] *= (1 + (variables['avg_income_raise']))
        
            outflows = {key: value * (1 + variables['avg_inflation_rate']) 
                        for key, value in outflows.items()}
            

            
 # Visualization           
plt.plot(pd.Series(assets_ending_list))
plt.xlabel('Month')
plt.ylabel('Ending Asset Value (x ₹10L)')
plt.show()   





