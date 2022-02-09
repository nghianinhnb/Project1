import datetime

class RequestDAO:
    def __init__(self, DAO):
        self.db = DAO
        self.db.table = 'request'

    # Thêm
    def request(self, uid, bid):
        q = self.db.query("INSERT INTO @table (`uid`, `bid`) VALUES ({}, {})"
                          .format(uid, bid))
        self.db.commit()

        return q

    def add_book(self, uid, bid):
        q = self.db.query("INSERT INTO @table (`uid`, `bid`, `status`) VALUES ({}, {}, 'COMPLETED')"
                          .format(uid, bid))
        self.db.commit()

        return q

    # Đọc
    def get_user_bids(self, uid):
        q = self.db.query("select bid from @table where uid={} and available=1 and status='COMPLETED' order by create_at DESC"
                          .format(uid))
        raw = q.fetchall()
        if raw:
            bids = [ bid[0] for bid in raw ]
            return bids
        return []

    def get_owner(self, bid):
        q = self.db.query("select uid from @table where bid={} and available=1 and status='COMPLETED'"
                          .format(bid))
        uid = q.fetchone()
        if uid:
            return uid[0]

    def get_requester_id(self, bid, available=1):
        q = self.db.query("select uid from @table where bid={} and available={} and status='WAITING'"
                          .format(bid, available))
        raw = q.fetchall()
        if raw:
            uids = [ uid[0] for uid in raw ]
            return uids
        return []

    def get_accepted_uid(self, bid):
        q = self.db.query("select uid from @table where bid={} and available=1 and status='ACCEPTED' order by create_at DESC limit 1"
                          .format(bid))
        uid = q.fetchone()
        if uid: return uid[0]
        return None

    def get_requesting_bids(self, uid):
        q = self.db.query("select bid from @table where uid={} and available=1 and status='WAITING' order by create_at DESC"
                          .format(uid))
        raw = q.fetchall()
        if raw:
            bids = [ bid[0] for bid in raw ]
            return bids
        return []

    def get_accepted_bids(self, uid):
        q = self.db.query("select bid from @table where uid={} and available=1 and status='ACCEPTED' order by create_at DESC"
                          .format(uid))
        raw = q.fetchall()
        if raw:
            bids = [ bid[0] for bid in raw ]
            return bids
        return []
    

    # Sửa
    def decline_request(self, uid, bid):
        q = self.db.query("UPDATE @table SET status='DECLINED', modify_at='{}' WHERE uid={} and bid={} and status='WAITING' and available=1"
                          .format(datetime.datetime.now(), uid, bid))
        self.db.commit()

        return q

    def decline_all(self, bid):
        q = self.db.query("UPDATE @table SET available=0, modify_at='{}' WHERE bid={} and status='WAITING' and available=1"
                          .format(datetime.datetime.now(), bid))
        self.db.commit()

        return q

    def accept_request(self, uid, bid):
        q = self.db.query("UPDATE @table SET status='ACCEPTED', modify_at='{}' WHERE uid={} and bid={} and status='WAITING' and available=1"
                          .format(datetime.datetime.now(), uid, bid))
        self.db.commit()

        return q

    def confirm(self, uid, bid):
        self.db.query("UPDATE @table SET available=0, modify_at='{}' WHERE bid={} and status='COMPLETED' and available=1"
                    .format(datetime.datetime.now(), bid))
        q = self.db.query("UPDATE @table SET status='COMPLETED', modify_at='{}' WHERE uid={} and bid={} and status='ACCEPTED' and available=1"
                          .format(datetime.datetime.now(), uid, bid))

        self.db.commit()

        return q

    def unconfirm(self, uid, bid):
        q = self.db.query("UPDATE @table SET status='DECLINED', available=0, modify_at='{}' WHERE uid={} and bid={} and status='ACCEPTED' and available=1"
                          .format(datetime.datetime.now(), uid, bid))

        self.db.commit()

        return q

    # Xoa
    # truong hop nguoi dung bam nham hoac doi y truoc khi chu so huu dong y yeu cau
    def cancel_request(self, uid, bid):
        q = self.db.query("DELETE FROM @table WHERE uid={} and bid={} and available=1 and status='WAITING'"
							.format(uid, bid))
        self.db.commit()
        if q : return True
        return False

