import datetime

class NotificationDAO:
    def __init__(self, DAO):
        self.db = DAO
        self.db.table = 'notification'

    # Thêm
    def make_notif(self, uid, message):
        q = self.db.query("INSERT INTO @table (`uid`, `message`) VALUES ({}, '{}')"
                          .format(uid, message))
        self.db.commit()

        return q

    def make_sys_notif(self, message):
        q = self.db.query("INSERT INTO @table (`message`) VALUES ('{}')"
                          .format(message))
        self.db.commit()

        return q


    # Đọc
    def get_unseen_notif(self, uid):
        q = self.db.query('SELECT * FROM @table WHERE uid = {} and is_unseen=1 order by create_at DESC'.format(uid))
        notif = q.fetchall()
        if notif:
            return notif
        else: return []

    def get_all_notif(self, uid):
        notif = self.get_unseen_notif(uid)

        q = self.db.query('SELECT * FROM @table WHERE uid = {} and is_unseen=0 order by create_at DESC'.format(uid))
        seen = q.fetchall()
        if seen:
            notif += seen

        return notif


    # Sửa
    def seen_notif(self, nid):
        q = self.db.query("UPDATE @table SET is_unseen=0, modify_at='{}' WHERE nid={}"
                          .format(datetime.datetime.now(), nid))
        self.db.commit()

        return q

    def seen_all_notif(self, uid):
        q = self.db.query("UPDATE @table SET is_unseen=0, modify_at='{}' WHERE uid={}"
                          .format(datetime.datetime.now(), uid))
        self.db.commit()

        return q