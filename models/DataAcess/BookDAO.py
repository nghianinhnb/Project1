import datetime

class BookDAO:
    def __init__(self, DAO):
        self.db = DAO
        self.db.table = 'book'

    # Thêm
    def add_book(self, book):
        title = book.title
        author = book.author
        publishyear = book.publishyear
        catalog = book.catalog
        review = book.review

        q = self.db.query("INSERT INTO @table (`title`, `author`, `publishyear`, `catalog`, `review`) VALUES ('{}', '{}', '{}', '{}', '{}')"
                          .format(title, author, publishyear, catalog, review))
        self.db.commit()

        q = self.db.query("SELECT bid FROM @table where title='{}' and author='{}' and publishyear='{}' and catalog='{}' and review='{}' order by create_at DESC"
                          .format(title, author, publishyear, catalog, review))
        bid = q.fetchone()[0]

        return bid


    # Đọc
    def get_all_books(self):
        q = self.db.query('SELECT * FROM @table order by create_at DESC')
        books = q.fetchall()

        return books

    def get_by_bid(self, bid):
        q = self.db.query('select * from @table where bid={}'.format(bid))
        book = q.fetchone()

        return book

    def search_by_author(self, author, limit=1000):
        q = self.db.query("select * from @table where author LIKE '%{}%' order by create_at DESC limit {}"
                          .format(author, limit))
        books = q.fetchall()

        return books

    def search_by_year(self, year, limit=1000):
        q = self.db.query("select * from @table where publishyear = '{}' order by create_at DESC limit {}"
                          .format(year, limit))
        books = q.fetchall()

        return books

    def search_by_catalog(self, catalog, limit=1000):
        q = self.db.query("select * from @table where catalog = '{}' order by create_at DESC limit {}"
                          .format(catalog, limit))
        books = q.fetchall()

        return books

    def search(self, text='', limit=1000):
        q = self.db.query("select * from @table where title LIKE '%{}%' \
                            or match(title, author) against('{}' WITH QUERY EXPANSION) \
                           and author not like '%{}%' limit {};"
                            .format(text, text, text, limit))
        books = q.fetchall()

        return books


    # Sửa
    def update(self, book):
        bid = book.bid
        title = book.title
        author = book.author
        publishyear = book.publishyear
        catalog = book.catalog 
        review = book.review
        available = book.available
        

        q = self.db.query("UPDATE @table SET title='{}', author='{}', publishyear='{}', catalog='{}', review='{}', available={}, modify_at='{}' WHERE bid={}"
                          .format(title, author, publishyear, catalog, review, available, datetime.datetime.now(), bid))
        self.db.commit()

        return q