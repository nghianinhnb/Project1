import mysql.connector

class DB:
    table = ''

    def __init__(self, app):
        self.db = mysql.connector.connect(
                  host=app.config['HOST'],
                  user=app.config['USER'],
                  password=app.config['PASSWORD'],
                  database=app.config['DATABASE']
                )

    def cur(self):
        cs = self.db.cursor()
        return cs

    def query(self, q):
        cs = self.cur()

        if len(self.table)>0 :
            q = q.replace("@table", self.table)

        cs.execute(q)
        return cs

    def commit(self):
        self.query("COMMIT;")