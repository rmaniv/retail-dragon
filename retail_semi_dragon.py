#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def simulate_portfolio(data_file, etf_name, benchmark=False):
    gld_df = pd.read_csv('data/GLD.csv', parse_dates=['Date'], index_col='Date')
    djp_df = pd.read_csv('data/DJP.csv', parse_dates=['Date'], index_col='Date')
    agg_df = pd.read_csv('data/AGG.csv', parse_dates=['Date'], index_col='Date')
    spy_df = pd.read_csv('data/SPY.csv', parse_dates=['Date'], index_col='Date')
    etf_df = pd.read_csv(data_file, parse_dates=['Date'], index_col='Date')

    df = pd.concat([
        spy_df['Close'].rename('SPY'),
        etf_df['Close'].rename(etf_name),
        gld_df['Close'].rename('GLD'),
        djp_df['Close'].rename('DJP'),
        agg_df['Close'].rename('AGG')
    ], axis=1)

    df = df.dropna()

    if benchmark:
        allocation = {
            'SPY': 0.60,
            'AGG': 0.40
        }
    else:
        allocation = {
            'SPY': 0.20,
            etf_name: 0.20,
            'GLD': 0.20,
            'DJP': 0.20,
            'AGG': 0.20
        }

    initial_fund = 100000  # Let's assume we start with $100,000
    initial_units = {}
    for etf, alloc in allocation.items():
        initial_units[etf] = (initial_fund * alloc) / df[etf].iloc[0]
        initial_units[etf] = int(round(initial_units[etf], 0))

    def rebalance_portfolio(current_units, current_prices, total_value, allocation):
        new_units = {}
        for etf, alloc in allocation.items():
            new_units[etf] = (total_value * alloc) / current_prices[etf]
            new_units[etf] = round(new_units[etf], 2)
        return new_units

    portfolio_values = []
    units_over_time = [initial_units]

    for i in range(len(df)):
        current_value = sum([units_over_time[-1][etf] * df[etf].iloc[i] for etf in allocation])
        portfolio_values.append(current_value)

        if i > 0 and df.index[i].month != df.index[i-1].month:
            new_units = rebalance_portfolio(units_over_time[-1], df.iloc[i], current_value, allocation)
            units_over_time.append(new_units)
        else:
            units_over_time.append(units_over_time[-1])

    portfolio_df = pd.DataFrame(portfolio_values, index=df.index, columns=['Portfolio_Value'])

    portfolio_df['Max_Value'] = portfolio_df['Portfolio_Value'].cummax()
    portfolio_df['Drawdown'] = ((portfolio_df['Portfolio_Value'] - portfolio_df['Max_Value']) / portfolio_df['Max_Value']) * 100

    if benchmark:
        return portfolio_df

    benchmark_df = simulate_portfolio(data_file, etf_name, benchmark=True)
    benchmark_df['Max_Value'] = benchmark_df['Portfolio_Value'].cummax()
    benchmark_df['Drawdown'] = ((benchmark_df['Portfolio_Value'] - benchmark_df['Max_Value']) / benchmark_df['Max_Value']) * 100

    plt.figure(figsize=(14, 7))
    plt.plot(portfolio_df.index, portfolio_df['Drawdown'], label=f'Portfolio with {etf_name}', color='blue')
    plt.plot(benchmark_df.index, benchmark_df['Drawdown'], label='60-40 SPY-AGG Portfolio', color='red', linestyle='--')
    plt.title('Drawdowns (%)')
    plt.xlabel('Date')
    plt.ylabel('Drawdown (%)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    max_drawdown_portfolio = portfolio_df['Drawdown'].min()
    max_drawdown_benchmark = benchmark_df['Drawdown'].min()

    years = (portfolio_df.index[-1] - portfolio_df.index[0]).days / 365.25

    cagr_portfolio = ((portfolio_df['Portfolio_Value'].iloc[-1] / portfolio_df['Portfolio_Value'].iloc[0]) ** (1 / years) - 1) * 100
    cagr_benchmark = ((benchmark_df['Portfolio_Value'].iloc[-1] / benchmark_df['Portfolio_Value'].iloc[0]) ** (1 / years) - 1) * 100

    time_period = f"{df.index[0].strftime('%Y-%m-%d')} to {df.index[-1].strftime('%Y-%m-%d')}"

    results_df = pd.DataFrame({
        'Metric': ['Max Drawdown (%)', 'CAGR (%)', 'Time Period (YYYY-MM-DD)'],
        f'Portfolio with {etf_name}': [round(max_drawdown_portfolio,2), round(cagr_portfolio,2), time_period],
        '60-40 SPY-AGG': [round(max_drawdown_benchmark,2), round(cagr_benchmark,2), time_period]
    }).set_index('Metric')

    return portfolio_df, results_df

portfolio_vxz, results_vxz = simulate_portfolio('data/VXZ.csv', 'VXZ')
portfolio_vixm, results_vixm = simulate_portfolio('data/VIXM.csv', 'VIXM')
portfolio_tail, results_tail = simulate_portfolio('data/TAIL.csv', 'TAIL')

combined_results = pd.concat([results_vxz, results_vixm, results_tail], axis=1)
print(combined_results)

combined_results.to_csv('results.csv')
