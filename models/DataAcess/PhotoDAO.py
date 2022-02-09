class PhotoDAO:
    def __init__(self, DAO):
        self.db = DAO
        self.db.table = "photo"

    # thêm
    def add_photo(self, bid, iurl):
        q = self.db.query("INSERT INTO @table (`bid`, `iurl`) VALUES ({}, '{}')".format(bid, iurl))
        self.db.commit()

        return q


    # đọc
    def get_cover(self, bid):
        q = self.db.query('SELECT iurl FROM @table where bid={} and cover=1'.format(bid))
        iurl = q.fetchone()
        if iurl: return [iurl[0]]
        else: return []

    def get_photos(self, bid):
        cover = self.get_cover(bid)

        q = self.db.query('SELECT iurl FROM @table where bid={} and cover=0'.format(bid))
        raw = q.fetchall()
        if raw:
            iurls = [ url[0] for url in raw ]
            return cover + iurls
        return cover


    # sửa
    def set_cover(self, bid, iurl):
        q = self.db.query("UPDATE @table SET cover=0 WHERE bid={}"
                          .format(bid))
        q = self.db.query("UPDATE @table SET cover=1 WHERE iurl='{}'"
                          .format(iurl))
        self.db.commit()

        return q


    # xóa
    def delete_photo(self, iurl):
        q = self.db.query("DELETE FROM @table WHERE iurl = '{}'"
							.format(iurl))
        self.db.commit()

        return q