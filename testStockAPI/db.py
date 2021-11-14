import psycopg2
from psycopg2 import Error
from json import dumps, loads, JSONDecodeError
from stockdata import Stockdata


def connection():
    con = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="incaroads",
        host="127.0.0.1",
        port="5433",
    )
    cur = con.cursor()
    return con, cur


def create_table():
    con, cur = connection()
    try:
        cur.execute(
            """CREATE TABLE ACCOUNTS
            (ACCOUNTNAME VARCHAR PRIMARY KEY NOT NULL,
            CASHBALANCE FLOAT NOT NULL,
            STOCKPORTFOLIO VARCHAR);"""
        )
    except Error as e:
        print(e)
    finally:
        if con:
            con.commit()
            con.close()


def delete_table():
    con, cur = connection()
    try:
        cur.execute("DROP TABLE ACCOUNTS;")
    except Error as e:
        print(e)
    finally:
        if con:
            con.commit()
            con.close()


def add_account(accountname, startingcash):
    con, cur = connection()
    try:
        cur.execute(
            """INSERT INTO ACCOUNTS
                    (ACCOUNTNAME,CASHBALANCE,STOCKPORTFOLIO)
                    VALUES (%s, %s, '{}');""",
            (accountname, startingcash),
        )
    except Error as e:
        print(e)
    finally:
        if con:
            con.commit()
            con.close()


def get_account(accountname):
    con, cur = connection()
    try:
        cur.execute("SELECT * FROM ACCOUNTS WHERE ACCOUNTNAME = %s", (accountname))
        row = cur.fetchone()
        return row
    except Error as e:
        print(e)
        return None
    finally:
        if con:
            con.commit()
            con.close()


def buy_stock(accountname, ticker, cash):
    con, cur = connection()
    ticker = ticker.upper()
    try:
        cur.execute("SELECT * FROM ACCOUNTS WHERE ACCOUNTNAME = %s", (accountname))
        row = cur.fetchone()
        if not row:
            raise ValueError("Account {} not found.".format(accountname))
        if cash > row[1]:
            raise ValueError("{} does not have {} in cash.".format(accountname, cash))
        try:
            portfolio = loads(row[2])
        except JSONDecodeError:
            portfolio = {}
        price = Stockdata(ticker).ask_price()
        if price is None:
            raise ValueError("Ticker {} is not available.".format(ticker))
        if price == 0:
            raise ValueError("No trading available now.")
        shares = cash / price
        if ticker in portfolio:
            portfolio[ticker] += shares
        else:
            portfolio[ticker] = shares
        cur.execute(
            """UPDATE ACCOUNTS SET CASHBALANCE = %s,
                    STOCKPORTFOLIO = %s""",
            (row[1] - cash, dumps(portfolio)),
        )
    except ValueError as e:
        print(e)
    finally:
        if con:
            con.commit()
            con.close()


def sell_stock(accountname, ticker, shares):
    con, cur = connection()
    ticker = ticker.upper()
    try:
        cur.execute("SELECT * FROM ACCOUNTS WHERE ACCOUNTNAME = %s", (accountname,))
        row = cur.fetchone()
        if not row:
            raise ValueError("Account {} not found.".format(accountname))
        try:
            portfolio = loads(row[2])
        except JSONDecodeError:
            portfolio = {}
        if ticker not in portfolio:
            raise ValueError("{} is not in {}'s portfolio.".format(ticker, accountname))
        if shares > portfolio[ticker]:
            raise ValueError(
                """{}'s portfolio does not have {} shares
                             of {}.""".format(
                    accountname, shares, ticker
                )
            )
        price = Stockdata(ticker).bid_price()
        if price is None:
            raise ValueError("Ticker {} is not available.".format(ticker))
        if price == 0:
            raise ValueError("No trading available now.")
        cash = price * shares
        portfolio[ticker] -= shares
        cur.execute(
            """UPDATE ACCOUNTS SET CASHBALANCE = %s,
                    STOCKPORTFOLIO = %s""",
            (row[1] + cash, dumps(portfolio)),
        )
    except ValueError as e:
        print(e)
    finally:
        if con:
            con.commit()
            con.close()
