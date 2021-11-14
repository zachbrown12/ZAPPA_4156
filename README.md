# ZAPPA_4156
4156 Group Project

<p>This project is an API for creating competitive stock-trading games, in which the owners of virtual stock portfolios with an initial cash balance at the game's start can compete by buying and selling shares of stock at real market prices to achieve the highest portfolio value by the game's end. It uses stock price data from Yahoo Finance, which means players' knowledge of the real stock market will be a competitive advantage.<p>

To install yfinance:<br/>
python -m pip install yfinance --upgrade --no-cache-dir<br/>

To install Django:<br/>
python -m pip install Django<br/>

To install rest-framework:<br/>
python -m pip install djangorestframework<br/>

To run the service:<br/>

1. migrate <br/>
python .\zappa\manage.py migrate <br/>
python .\zappa\manage.py makemigrations <br/>
python .\zappa\manage.py migrate <br/>

2. run server <br/>
python .\zappa\manage.py runserver<br/>
  
To use the service:<br/>
  
Using the resource path http://127.0.0.1:8000/,
  
<b>POST</b>   /api/newgame/ -- Creates a new game. Takes optional parameters "title", "rules", and "starting_balance". <br/>
<b>POST</b>   /api/addnewportfolio/{game_id} -- Adds a new portfolio to the game with ID {game_id}. Takes optional parameter "title".<br/>
<b>POST</b>   /api/addexistingportfolio/{game_id} -- Adds an existing portfolio with ID "portfolio_id" to the game with ID {game_id}. Requires parameter "portfolio_id".<br/>
<b>POST</b>   /api/removeportfolio/{game_id} -- Removes the portfolio with ID "portfolio_id" from the game with ID {game_id}. Requires parameter "portfolio_id".<br/>
<b>GET</b>   /api/games/{game_id} -- Returns the current status of the game with ID {game_id} and the portfolios within, including the values and rankings of its portfolios using stock bid prices at the time called.<br/>
<b>GET</b>   /api/games/ -- Returns the current status of all games and the portfolios within, including the values and rankings of portfolios within each game using stock bid prices at the time called.<br/>   
   
<b>GET</b>   /api/portfolios/ -- Returns the current status of all portfolios, including the current value of each using stock bid prices at the time called.<br/>
<b>GET</b>   /api/portfolio/{portfolio_id} -- Returns the current status of the portfolio with ID {portfolio_id}, including its current value using stock bid prices at the time called.<br/>
<b>POST</b>   /api/newportfolio/ -- Creates a new portfolio without assigning it to a game. Takes optional parameter "title".<br/>
<b>POST</b>   /api/buystock/{portfolio_id} -- Buys "shares" shares of the stock with ticker "ticker" at its current ask price, adds it to the portfolio with ID {portfolio_id}, and deducts the cost from the portfolio's cash_balance. Requires parameters "ticker" and "shares".<br/>
<b>POST</b>   /api/sellstock/{portfolio_id} -- Sells "shares" shares of the stock with ticker "ticker" at its current bid price, removes those shares from the portfolio with ID {portfolio_id}, and adds the proceeds to the portfolio's cash_balance. Requires parameters "ticker" and "shares".<br/>
   
<b>GET</b>   /api/holdings/ -- Returns all stock holdings in the database.<br/>
<b>GET</b>   /api/holdings/{holding_id} -- Returns the holding with ID {holding_id}.<br/>
<b>GET</b>   /api/transactions/ -- Returns a list of all transaction records in the database.<br/>
<b>GET</b>   /api/transactions/{transaction_record} -- Returns the transaction record with ID {transaction_record}.<br/>
