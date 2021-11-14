import db

# TODO: this needs to be re-implemented as an actual test suite
db.delete_table()
db.create_table()
db.add_account("test_account", 1000.0)

db.buy_stock("test_account", "aapl", 100.0)
print(db.get_account("test_account"))
db.buy_stock("test_account", "aapl", 50.0)
print(db.get_account("test_account"))
db.buy_stock("test_account", "tsla", 100.0)
print(db.get_account("test_account"))
db.sell_stock("test_account", "AAPL", 0.5)
print(db.get_account("test_account"))
