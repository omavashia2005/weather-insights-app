import sqlite3

con = sqlite3.connect("tutorial.db")
cur = con.cursor()
# creating the table
cur.execute("CREATE TABLE movie(title, year, score)")

# storing result
res = cur.execute("SELECT name FROM sqlite_master where name='spam'")

# executing one "commit"
cur.execute(""
            "insert into movie values"
            "('Monty Python and the Holy Grail', 1975, 8.2), "
            "('And Now for Something Completely Different', 1971, 7.5)")

# commiting
con.commit()
# selecting certain data
res = cur.execute("select score from movie")

# fetching all results
print(res.fetchall())

# executing many
data = [
    ('Burn!', 1999, 9.0),
    ('The Godfather', 2001, 9.2),
    ('Scarface', 2000, 9.1)
]

cur.executemany("insert into movie values(?, ?, ?)", data)

#commiting
con.commit()

# confirming all entries have been written to the disk
con.close()

new_con = sqlite3.connect("tutorial.db")
new_cur = new_con.cursor()

res = new_cur.execute("select title, year from movie order by score desc")
title, year = res.fetchone()

print(f'The highest scoring Monty Python movie is {title!r}, released in {year}')
new_con.close()
