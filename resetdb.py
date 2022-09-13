import sqlite3

con = sqlite3.connect('database.db')
cur = con.cursor()
qry = ('''DELETE FROM MESSAGES;''')
cur.execute(qry)

con.commit()
print("All Messages Cleared!")
cur.close()
con.close()