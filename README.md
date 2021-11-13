# ZAPPA_4156
4156 Group Project

<p>This project is an API for creating competitive stock-trading games, in which the owners of virtual stock portfolios with an initial cash balance at the game's start can compete by buying shares of stock at real market prices to achieve the highest portfolio value by the game's end. It uses stock price data from Yahoo Finance, which means players' knowledge of the real stock market will be a competitive advantage.<p>

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

   http://127.0.0.1:8000/api/newgame/ -- Creates a new game. Takes optional data for "title", "rules", and "starting_balance". <br/>
   http://127.0.0.1:8000/api/addnewportfolio/<i>game_id</i> -- Adds a new portfolio to the game with ID <i>game_id</i>. Takes optional data for "title".<br/>
   http://127.0.0.1:8000/api/addexistingportfolio/<i>game_id</i> -- Adds an existing portfolio with ID "portfolio_id" to the game with ID <i>game_id</i>. Requires data for "portfolio_id".<br/>
   http://127.0.0.1:8000/api/removeportfolio/<i>game_id</i> -- Removes the portfolio with ID "portfolio_id" from the game with ID <i>game_id</i>. Requires data for "portfolio_id".<br/>
   http://127.0.0.1:8000/api/games/<i>game_id</i> -- Returns the current status of the game with ID <i>game_id</i> and the portfolios within, including the values and ranking of its portfolios using stock bid prices at the time called.<br/>   
   http://127.0.0.1:8000/api/games/ -- Returns the current status of all games and the portfolios within, including the values and ranking of portfolios within each game using stock bid prices at the time called.<br/>   
   
   http://127.0.0.1:8000/api/portfolios/ -- Returns the current status of all portfolios, including the current value of each using stock bid prices at the time called.<br/>
   http://127.0.0.1:8000/api/portfolio/<i>portfolio_id</i> -- Returns the current status of the portfolio with ID <i>portfolio_id</i>, including its current value using stock bid prices at the time called.<br/>
   http://127.0.0.1:8000/api/newportfolio/ -- Creates a new portfolio without assigning it to a game. Takes optional data for "title".<br/>
   http://127.0.0.1:8000/api/buystock/<i>portfolio_id</i> -- Buys "shares" shares of the stock with ticker "ticker" at its current ask price, adds it to the portfolio with ID <i>portfolio_id</i>, and deducts the cost from the portfolio's cash_balance. Requires data for "ticker" and "shares".<br/>
   http://127.0.0.1:8000/api/sellstock/<i>portfolio_id</i> -- Sells "shares" shares of the stock with ticker "ticker" at its current bid price, removes those shares from the portfolio with ID <i>portfolio_id</i>, and adds the proceeds to the portfolio's cash_balance. Requires data for "ticker" and "shares".<br/>
   
   http://127.0.0.1:8000/api/holdings/ -- Returns all stock holdings in the database.<br/>
   http://127.0.0.1:8000/api/holdings/<i>holding_id</i> -- Returns the holding with ID <i>holding_id</i>.<br/>
   http://127.0.0.1:8000/api/transactions/ -- Returns a list of all transaction records in the database.<br/>
   http://127.0.0.1:8000/api/transactions/<i>transaction_record</i> -- Returns the transaction record with ID <i>transaction_record</i>.<br/>
