# Super Simple Stock Market Assignment

This python console application is a “Super Simple Stock Market”, allowing the operator to log trades and perform simple stock data analysis.

## Getting started
Requirements:
- Python 3.10
- PIP

Start the application by running:
```sh 
python main.py
```
#### Testing

Use the following command from the project root to run tests:
```sh 
python -m unittest
```

## Task Requirements
Provide working source code that will:

1. For a given stock,
   - Given any price as input, calculate the dividend yield 
   - Given any price as input, calculate the P/E Ratio
   - Record a trade, with timestamp, quantity of shares, buy or sell indicator and traded price
   - Calculate Volume Weighted Stock Price based on trades in past 15 minutes
2. Calculate the GBCE All Share Index using the geometric mean of prices for all stocks

#### Sample data from the Global Beverage Corporation Exchange
| Stock Symbol | Type      | Last Dividend | Fixed Dividend | Par Value |
|--------------|-----------|---------------|----------------|-----------|
| TEA          | Common    | 0             |                | 100       |
| POP          | Common    | 8             |                | 100       |
| ALE          | Common    | 23            |                | 60        |
| GIN          | Preferred | 8             | 2%             | 100       |
| JOE          | Common    | 13            |                | 250       |

