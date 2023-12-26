import sqlite3
import codecs
import re

conn = sqlite3.connect('extraction.db')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS EXTRACTION(id INTEGER PRIMARY KEY, posologie TEXT)')

concord = codecs.open("corpus-medical_snt/concord.html", "r", "utf-8")
liste = list(concord)
j = 1

for i in liste:
    poso = re.search('<a href=\".+\">(.+)</a>',i)
    if poso:
        tmp = poso.group(1)
        if tmp.startswith(','):
            tmp = tmp[2:]
        c.execute('INSERT INTO EXTRACTION VALUES(\''+str(j)+'\', \''+tmp+'\')')
    j = j + 1

conn.commit()
c.close()
conn.close()
