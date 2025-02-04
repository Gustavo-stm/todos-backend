import sqlite3

connexion = sqlite3.connect('to_do_list.db', autocommit = True)
cur = connexion.cursor()

res = cur.execute('SELECT * FROM mytodos')

[print(i) for i in res]



