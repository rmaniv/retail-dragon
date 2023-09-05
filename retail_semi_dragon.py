#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Function to load ETF data and simulate the portfolio
def simulate_portfolio(data_file, etf_name):
    # Load the data for each ETF
    gld_df = pd.read_csv('data/GLD.csv', parse_dates=['Date'], index_col='Date')
    djp_df = pd.read_csv('data/DJP.csv', parse_dates=['Date'], index_col='Date')
    agg_df = pd.read_csv('data/AGG.csv', parse_dates=['Date'], index_col='Date')
    spy_df = pd.read_csv('data/SPY.csv', parse_dates=['Date'], index_col='Date')
    etf_df = pd.read_csv(data_file, parse_dates=['Date'], index_col='Date')

    # Combine the close prices of each ETF into one dataframe
    df = pd.concat([
        spy_df['Close'].rename('SPY'),
        etf_df['Close'].rename(etf_name),
        gld_df['Close'].rename('GLD'),
        djp_df['Close'].rename('DJP'),
        agg_df['Close'].rename('AGG')
    ], axis=1)

    ## Remove rows with NaN values
    df = df.dropna()

    # Initial allocation
    initial_fund = 100000  # Let's assume we start with $100,000
    allocation = {
        'SPY': 0.20,
        etf_name: 0.20,
        'GLD': 0.20,
        'DJP': 0.20,
        'AGG': 0.20
    }

    # Calculate the number of units for each ETF based on the allocation and initial prices
    initial_units = {}
    for etf, alloc in allocation.items():
        initial_units[etf] = (initial_fund * alloc) / df[etf].iloc[0]
        initial_units[etf] = int(round(initial_units[etf], 0))

    # Function to rebalance the portfolio based on the allocation
    def rebalance_portfolio(current_units, current_prices, total_value, allocation):
        new_units = {}
        for etf, alloc in allocation.items():
            new_units[etf] = (total_value * alloc) / current_prices[etf]
            # Ensure fractional ownership up to owning 1% of a share is allowed
            new_units[etf] = round(new_units[etf], 2)
        return new_units

    # Simulate the portfolio over time
    portfolio_values = []
    units_over_time = [initial_units]

    for i in range(len(df)):
        # Calculate current value of the portfolio
        current_value = sum([units_over_time[-1][etf] * df[etf].iloc[i] for etf in allocation])
        portfolio_values.append(current_value)

        # Rebalance at the start of each month
        if i > 0 and df.index[i].month != df.index[i-1].month:
            new_units = rebalance_portfolio(units_over_time[-1], df.iloc[i], current_value, allocation)
            units_over_time.append(new_units)
        else:
            units_over_time.append(units_over_time[-1])

    # Convert to a dataframe for easier plotting later
    portfolio_df = pd.DataFrame(portfolio_values, index=df.index, columns=['Portfolio_Value'])

    # Calculate drawdowns for the portfolio
    portfolio_df['Max_Value'] = portfolio_df['Portfolio_Value'].cummax()
    portfolio_df['Drawdown'] = ((portfolio_df['Portfolio_Value'] - portfolio_df['Max_Value']) / portfolio_df['Max_Value']) * 100

    # Calculate drawdowns for plain vanilla SPY
    df['SPY_Max_Value'] = df['SPY'].cummax()
    df['SPY_Drawdown'] = ((df['SPY'] - df['SPY_Max_Value']) / df['SPY_Max_Value']) * 100

    # Plotting
    plt.figure(figsize=(14, 7))
    plt.plot(portfolio_df.index, portfolio_df['Drawdown'], label=f'Portfolio with {etf_name}', color='blue')
    plt.plot(df.index, df['SPY_Drawdown'], label='SPY', color='red', linestyle='--')
    plt.title('Drawdowns (%)')
    plt.xlabel('Date')
    plt.ylabel('Drawdown (%)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Calculate max drawdown for the portfolio and SPY
    max_drawdown_portfolio = portfolio_df['Drawdown'].min()
    max_drawdown_spy = df['SPY_Drawdown'].min()

    # Calculate CAGR for the portfolio and SPY
    years = (portfolio_df.index[-1] - portfolio_df.index[0]).days / 365.25  # approximate number of days in a year including leap years

    cagr_portfolio = ((portfolio_df['Portfolio_Value'].iloc[-1] / portfolio_df['Portfolio_Value'].iloc[0]) ** (1 / years) - 1) * 100
    cagr_spy = ((df['SPY'].iloc[-1] / df['SPY'].iloc[0]) ** (1 / years) - 1) * 100

    # Calculate time period
    time_period = f"{df.index[0].strftime('%Y-%m-%d')} to {df.index[-1].strftime('%Y-%m-%d')}"

    # Compile results into a DataFrame for display
    results_df = pd.DataFrame({
        'Metric': ['Max Drawdown (%)', 'CAGR (%)', 'Time Period (YYYY-MM-DD)'],
        f'Portfolio with {etf_name}': [round(max_drawdown_portfolio,2), round(cagr_portfolio,2), time_period],
        f'SPY_{etf_name}': [round(max_drawdown_spy,2), round(cagr_spy,2), time_period]
    }).set_index('Metric')

    return portfolio_df, results_df

# Simulate the portfolios for VXZ, VIXM, and TAIL
portfolio_vxz, results_vxz = simulate_portfolio('data/VXZ.csv', 'VXZ')
portfolio_vixm, results_vixm = simulate_portfolio('data/VIXM.csv', 'VIXM')
portfolio_tail, results_tail = simulate_portfolio('data/TAIL.csv', 'TAIL')

# Merge the portfolio dataframes
combined_portfolio = pd.concat([portfolio_vxz, portfolio_vixm, portfolio_tail], axis=1)

# Merge the results dataframes
combined_results = pd.concat([results_vxz, results_vixm, results_tail], axis=1)
print(combined_results)

# Save the combined results in a .csv file
combined_results.to_csv('results.csv')
