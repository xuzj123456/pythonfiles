In order to construct our backtest model, we need to use class Data_obtain and class BackTestModel in Model.py file. 

The class Data_obtain is used to obtain data, we need imput the path data stored, which we have provided in the zip file, 
and you need to put the data in the same directory with the Python file. 
We could also import the start date and end date, whose default settings are '20100101' and '20200101' respectively. 

When we initiate a BackTestModel object, we need input a Data_obtain object. You could write your own trading strategy and 
stock selecting strategy in strategy() method and select_stock() method.
If you want to buy shares of a stock, you could use method Add_Open, and input parameters date, the number of shares you 
want to buy, code of stock, the price of the stock shares when you buy.
If you want to sell shares of stock you hold, you could use method Sell,  and input parameters date, the number of shares you 
still want to hold, code of stock, the price of the stock shares when you sell. It is important that you should import the number of
shares you still want to hold, but not the number of shares you want to sell.
You could also add some methods into this class if you need, but had better not modify the methods __init__, Add_Open, Sell, 
stop_profit, stop_loss, Update, Cacul_Performance, these models would make sure the model function well. 
Parameter method has some default settings about parameters, including trading fee rate, slippage, original capital, stop profit rate, 
stop loss rate and so on. If you want to change these parameters, you could modify the default settings of this method.

After the strategies are designed, you need to initiate a BackTestModel object, and call out the Run method, then the backtest
procedure would begin, and the model would automatically calculate the total return, annual return, volatility, sharpe ratio, 
sortino ratio, max drawdown ratio, etc, and would also draw a picture about your return curve, compared to several index curve
in the same diagram.