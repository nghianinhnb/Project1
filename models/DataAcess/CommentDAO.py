import datetime

class CommentDAO:
    def __init__(self, DAO):
        self.db = DAO
        self.db.table = 'comment'

    # Thêm
    def add_comment(self, uid, bid, text):
        q = self.db.query("INSERT INTO @table (`uid`, `bid`, `text`) VALUES ({}, {}, '{}')"
                          .format(uid, bid, text))
        self.db.commit()

        return q


    # Đọc
    def get_comments(self, bid):
        q = self.db.query('SELECT * FROM @table WHERE bid = {} and available=1 order by create_at DESC'.format(bid))
        cmts = q.fetchall()

        return cmts


    # Sửa
    def edit_comment(self, cid, text):
        q = self.db.query("UPDATE @table SET text='{}', modify_at='{}' WHERE cid={}"
                          .format(text, datetime.datetime.now(), cid))
        self.db.commit()

        return q

    def hide_comment(self, cid):
        q = self.db.query("UPDATE @table SET available=0, modify_at='{}' WHERE cid={}"
                          .format(datetime.datetime.now(), cid))
        self.db.commit()

        return q