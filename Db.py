import psycopg2
import urllib.parse as urlparse
import os

class Db():
    def __init__(self):
        url = urlparse.urlparse(os.environ['DATABASE_URL'])
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port
        self.conn = psycopg2.connect(dbname=dbname,user=user,password=password,host=host,port=port)

    def fetchAll(self, c):
        curr = c.fetchone()
        result = []
        while curr != None:
            result.append(curr)
            curr = c.fetchone()
        return result

    def allItems(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM ITEMS WHERE SEEN = 0")
        return self.fetchAll(c)

    def newPlayer(self, name):
        c = self.conn.cursor()
        c.execute("SELECT * FROM PLAYERS WHERE NAME = %s",(name,))
        if c.fetchone() != None:
            return -1
        c.execute("INSERT INTO PLAYERS VALUES (%s,%s)",(name,0))
        self.conn.commit()
        return 1

    def removeItem(self, name):
        c = self.conn.cursor()
        c.execute("UPDATE ITEMS SET SEEN = 1 WHERE NAME = %s",(name,))
        self.conn.commit()
        return 1

    def editTokens(self, name, adjust):
        c = self.conn.cursor()
        c.execute("SELECT * FROM PLAYERS WHERE NAME = %s",(name,))
        tokens = c.fetchone()[1] + adjust
        c.execute("UPDATE PLAYERS SET TOKENS = %s WHERE NAME = %s",(tokens,name))
        self.conn.commit()

    def allPlayers(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM PLAYERS")
        return self.fetchAll(c)

    def playerTokens(self, name):
        c = self.conn.cursor()
        c.execute("SELECT * FROM PLAYERS WHERE NAME = %s",(name,))
        player = c.fetchone()
        if player == None:
            return -1
        else:
            return player[1]

    def newItem(self, name, description):
        c = self.conn.cursor()
        c.execute("SELECT * FROM ITEMS WHERE NAME = %s",(name,))
        if c.fetchone() != None:
            return None
        c.execute("INSERT INTO ITEMS VALUES (%s,%s,%s)",(name,description,0))
        self.conn.commit()

if __name__ == "__main__":
    # override run used to add to the server
    f = open("data.txt")
    raw = f.read()
    f.close()
    db = Db()
    items = raw.split("\n\n")
    items = list(map(lambda x: x.split("\n"),items))
    for item in items:
        db.newItem(item[0],item[1])
