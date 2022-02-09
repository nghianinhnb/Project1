from app import dao as DAO, app
from copy import copy
from os.path import join
from uuid import uuid4

class Book:
    def __init__(self, bid=None):
        self.dao = copy(DAO)
        if bid:
            book_info = self.dao.book.get_by_bid(bid)
            if book_info:
                self.bid = book_info[0]
                self.uid = self.dao.request.get_owner(self.bid)
                self.title = book_info[1]
                self.author = book_info[2]
                self.publishyear = book_info[3]
                self.catalog = book_info[4]
                self.review = book_info[5]
                self.available = book_info[6]
                self.photos = self.get_photos(self.bid)

    def get_follower_id(self):
        uids = self.dao.follow.get_follower(self.bid)
        return uids

#    def get_follower(self):
#        uids = self.get_follower_id()
#        users = [ self.dao.user.get_by_id() for id in uids ]
#        return users

    def get_requester_id(self, available=1):
        uids = self.dao.request.get_requester_id(self.bid, available)
        return uids

    def get_requester(self):
        uids = self.get_requester_id()
        users = [ self.dao.user.get_by_id(uid) for uid in uids ]
        return users

    def update(self, new_photos=[]):
        self.dao.book.update(self)
        for photo in new_photos:
            self.dao.photo.add_photo(self.bid, photo)

    def add_book(self, uid):
        bid = self.dao.book.add_book(self)
        for photo in self.photos:
            self.dao.photo.add_photo(bid, photo)
        self.dao.request.add_book(uid, bid)
        return bid

    def save_photo(self, image):
        path = app.config['PHOTOS_SAVE_PATH']
        filename = uuid4().hex + '_raw.png'
        image.save(join(path, filename))
        return filename

    def get_photos(self, bid):
        return self.dao.photo.get_photos(bid)

    def delete_photo(self, photo):
        return self.dao.photo.delete_photo(photo)

    def set_cover(self, photo):
        return self.dao.photo.set_cover(self.bid, photo)

    def get_all_books(self):
        return self.dao.book.get_all_books()

    def search_by_author(self, author, limit):
        return self.dao.book.search_by_author(author=author, limit=limit)

    def search_by_year(self, year, limit):
        return self.dao.book.search_by_year(year=year, limit=limit)

    def search_by_catalog(self, catalog, limit):
        return self.dao.book.search_by_catalog(catalog=catalog, limit=limit)

    def search(self, text, limit):
        return self.dao.book.search(text=text, limit=limit)

    def decline_all(self):
        return self.dao.request.decline_all(self.bid)

    def get_accepted_uid(self):
        uid = self.dao.request.get_accepted_uid(self.bid)
        return uid

    def add_comment(self, uid, text):
        if text:
            self.dao.comment.add_comment(uid=uid, bid=self.bid, text=text)

    def get_comments(self):
        return self.dao.comment.get_comments(self.bid)

    def edit_comment(self, text, cid):
        return self.dao.comment.edit_comment(text, cid)

    def hide_comment(self, cid):
        return self.dao.comment.hide_comment(cid)