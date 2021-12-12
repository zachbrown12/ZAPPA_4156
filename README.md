# ZAPPA_4156 Group Project: Trade Simulation

<h2>Overview</h2>

<p>This project is a combination of a front-end program and a back-end API server for creating competitive stock-trading games. Using our service, the owners of virtual stock portfolios with an initial cash balance at the game's start can compete by buying and selling shares of stock at real market prices to achieve the highest portfolio value by the game's end. It uses stock price data from Yahoo Finance, which means players' knowledge of the real stock market will be a competitive advantage.<p>  

<h2>Online Program</h2>

<p>We host the back-end API server on Heroku, but the client runs on "localhost".<p>

<h3>Back-end API endpoint</h3>
https://zappa-api.herokuapp.com/api

<h3>Client app</h3>
The following installation section explains how to run the client on "localhost".

<h2>Local Installation</h2>

<h3>Installation of required packages</h3>

This repository does not include third-party code other than the auto-generated skeleton code generated by django-admin startproject. Stock data is obtained from Yahoo Finance, using the yfinance python package. We are using AWS to host our postgresql database. This means a few packages need to be installed before use.<br/>

1. To install all required python packages:<br/>
pip install -r .\requirements.txt<br/>

2. To install all required packages for front-end:<br/>
cd .\reactfrontend <br/>
npm install

<h3>How to run the program</h3>

1. run backend server <br/>
python .\manage.py runserver<br/>

2. run client app <br/>
cd .\reactfrontend <br/>
npm start

<h2>Architecture and Technology</h2>

<h3>Architecture v2.0</h3>

<img src="images/architecture.png" width="600" />
 
<h3>Database v2.0</h3>

<img src="images/db.png" width="1000" />

<h3> Source code </h3>

Our main application logic is contained within the following files:
<ul>
  <li>api/helpers.py</li> 
  <li>api/serializers.py</li>
  <li>api/urls.py</li>
  <li>api/utils.py</li>
  <li>api/views.py</li>
  <li>trade_simulation/models.py</li>
  <li>users/models.py</li>
  <li>users/urls.py</li>
  <li>users/views.py </li>
</ul>

<h3> Continuous integration  </h3>

We are using <a href="https://circleci.com/">CircleCI</a> for continuous integration of unit tests, system tests, and style checking. These occur automatically upon commit in GitHub. The outputs are stored in CircleCI's "artifacts" area for each commit. 
Additionally, we are using <a href="https://sonarcloud.io/">SonarCloud</a> for static analysis, which occurs upon pull request to main branch in GitHub.

<ul style="list-style-type:none">
<li><h4> Unit tests </h4>
To see the results of our unit tests, check our htmlcov/ files in the repo for a current example, or run: coverage run --source='.' manage.py test .<br/>
Currently our branch coverage is at 92%.<br/></li>

<li><h4> System tests </h4>
We have a suite of system tests using Postman, under the <a href="https://columbia-university-student-plan-team-187884.postman.co/workspace/ZAPPA~414bd806-3ab6-4b69-8800-28b2145f10ca/collection/14941238-038eb57b-2eae-4982-9dc1-a5c505356fce">ZAPPA workspace</a>, called "Zappa System Tests." This sequence of requests tests success and possible failure conditions for all use cases of our API, and can also be run manually.<br/></li>

<li><h4>Style compliance</h4>
We are using flake8 for Python style checking; the output file for this is in bugs.txt which is empty.<br/>
To run the tests for flake8 you may run python3 -m flake8 --extend-exclude=./.venv,./zappa/.venv > bugs.txt  <br/></li>

<li><h4>Static analysis</h4>
We are using SonarCloud to check our code for bugs, vulnerabilities, security hotspots, and code smells.<br/> 
Additionally, we are using SonarLint to catch a limited subset of these issues instantly in VSCode.</li>
SonarCloud does not generate a report document, but we have screen-captured a sample status report from sonarcloud.io for our main branch in the file SonarCloudReport.jpg.
</ul>

<h2>Available endpoints for the backend API service</h2>

Using the resource path http://zappa-api.herokuapp.com, the following methods are available:<br/>

<h4>Games</h4>
Each Game contains Portfolios that compete against each other to attain the highest value. A Game has a "title" (a string of maximum length 200), "rules" (a string of maximum length 200), a "starting_balance" (a floating-point number less than 10<sup>14</sup>, with two decimal digits) that all portfolios within the game are initialized with, and a "winner" to be determined.<br/><br/>

<b>GET</b>   /api/games/ -- Returns the current status of all games and the portfolios within, including the values and rankings of portfolios within each game, using stock bid prices at the time called.<br/>

<b>GET</b>   /api/game/{game_title} -- Returns the current status of the game with title {game_title} and the portfolios within, including the values and rankings of its portfolios, using stock bid prices at the time called.
<blockquote><i> Example: /api/game/test game 1 </blockquote></i>

<b>POST</b>   /api/game/{game_title} -- Creates a new game with title {game_title}. Takes optional body parameters "rules" and "startingBalance" (default 10000.0).
<blockquote><i> Example: /api/game/test game 2 </br> Body: {"rules": "All's fair in love and war", "startingBalance": "30000.0"} </blockquote></i>

<b>DELETE</b>   /api/game/{game_title} -- Deletes the game with title {game_title}. 
<blockquote><i> Example: /api/game/test game 2 </blockquote></i>

<h4>Portfolios</h4>
Each Portfolio contains Holdings of stocks in various amounts. A Portfolio has a "title" (a string of maximum length 200), a "cash_balance" (a floating-point number less than 10<sup>14</sup>, with two decimal digits), a "total_value" computed from stock holdings plus cash balance, and a "game_rank" determined by how its total_value stacks up against other Portfolios in the same Game.<br/><br/>

<b>GET</b>   /api/portfolios/ -- Returns the current status of all portfolios, including the current total_value of each, using stock bid prices at the time called.<br/>

<b>GET</b>   /api/portfolio/{game_title}/{port_title} -- Returns the current status of the portfolio from {game_title} with the title {port_title}, including its current total_value, using stock bid prices at the time called.<br/>
<blockquote><i>Example: /api/portfolio/test game 1/portfolio 1</blockquote></i>

<b>POST</b>   /api/portfolio/{game_title}/{port_title} -- Creates a portfolio in game {game_title} with title {port_title}, with a starting cash_balance equal to the game's starting_balance.<br/>
<blockquote><i>Example: /api/portfolio/test game 1/portfolio 2</blockquote></i>

<b>DELETE</b>   /api/portfolio/{game_title}/{port_title} -- Deletes the portfolio from {game_title} with title {port_title}.<br/>
<blockquote><i>Example: /api/portfolio/test game 1/portfolio 2</blockquote></i>

<b>POST</b>   /api/portfolio/trade -- Performs a transaction on a portfolio. This can be one of two types depending on body parameters:
<ul style="list-style-type:none">
<li>
 
 If the value of the required parameter "securityType" is "stock", then parameters "portfolioTitle" (string), "gameTitle" (string), "ticker" (string), and "shares" (float) are required. If the value of "shares" is positive, the portfolio in game "gameTitle" with title "portfolioTitle" will buy "shares" shares of the stock with ticker "ticker". If the value of "shares" is negative, that portfolio will sell "shares" shares of that stock instead.
<blockquote><i> Example: /api/portfolio/trade </br> Body: {"portfolioTitle": "portfolio 1", "gameTitle": "test game 1", "securityType": "stock", "ticker":"AAPL", "shares":50.0} </blockquote></i>

Also, if the value of the optional parameter "exercise" is a contract symbol of an option in the portfolio that can be exercised to transact "shares" shares of the stock with ticker "ticker" at a different price, then that option will be exercised, and the quantity of that option in the portfolio will be correctly deducted.
<blockquote><i> Example: /api/portfolio/trade </br> Body: {"portfolioTitle": "portfolio 1", "gameTitle": "test game 1", "securityType": "stock", "ticker":"TSLA", "shares":-10.0, "exercise":"TSLA211231P01115000"} </blockquote></i>
</li>

<li>
 
 If the value of the required parameter "securityType" is "option", then parameters "portfolioTitle" (string), "gameTitle" (string), "contract" (string), and "quantity" (float) are required. If the value of "quantity" is positive, the portfolio in game "gameTitle" with title "portfolioTitle" will buy "quantity" amount of options with contract "contract". If the value of "quantity" is negative, that portfolio will sell "quantity" options with that contract instead. <br/>
<blockquote><i> Example: /api/portfolio/trade </br> Body: {"portfolioTitle": "portfolio 1", "gameTitle": "manual test game 1", "securityType": "option", "contract":"AAPL211223C00148000", "quantity":-1.0} </blockquote></i>
</li>
</ul>

<h4>Holdings</h4>
Each Holding represents shares of a stock held in a portfolio. A Holding has a "ticker" (a 4-5 character string representing a valid stock ticker) and a quantity "shares" (a floating-point number less than 10<sup>14</sup>, with two decimal digits).<br/><br/>

<b>GET</b>   /api/holdings/ -- Returns all stock holdings in the database.<br/>

<b>GET</b>   /api/holding/{port_title}/{game_title}/{ticker} -- Returns the holding in the portfolio {port_title} within the game {game_title} that has the ticker {ticker}.<br/>
<blockquote><i>Example: /api/holding/portfolio 1/test game 1/AAPL</blockquote></i>

<h4>Options</h4>
Each Option represents the ability to either buy or sell shares of a stock at a specific strike price before its expiration date. An Option has a "contract" (a string of max length 25 representing the standard contract symbol containing the essential info about the option), and a value "quantity" a floating-point number less than 10<sup>12</sup>, with two decimal digits). One stock option (quantity 1.0) can be used to trade 100 shares.<br/><br/>

<b>GET</b>   /api/options/ -- Returns all stock options in the database.<br/>

<b>GET</b>   /api/option/{port_title}/{game_title}/{contract} -- Returns the option in the portfolio {port_title} within the game {game_title} that has the contract symbol {contract}.<br/>
<blockquote><i>Example: /api/option/portfolio 1/test game 1/AAPL211223C00148000</blockquote></i>

<h4>Transactions</h4>
Each Transaction is a record of a transaction performed by a portfolio. A Transaction may record a portfolio buying or selling stock with or without exercising options, or buying or selling options. A Transaction has a "ticker", a "trade_type" depending on what was performed, a quantity "shares", and a "bought_price" recording the price at the time of transaction.<br/><br/>

<b>GET</b>   /api/transactions/ -- Returns all transaction records in the database.<br/>

<b>GET</b>   /api/transaction/{uid} -- Returns the transaction record with uid {uid}.<br/>
<blockquote><i>Example: /api/transaction/c971b071-7d59-4d96-be9b-710a463c0fb7</blockquote></i>


