from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, login, dao as DAO
from copy import copy
from datetime import datetime
from math import floor
from time import time
import jwt
from flask import url_for
from controllers.Book import Book

class User(UserMixin):
    id = None

    def __init__(self, id = None, email = None, name = None):
        self.dao = copy(DAO)
        user_info = None
        if id : user_info = self.dao.user.get_by_id(id)
        elif email : user_info = self.dao.user.get_by_email(email)
        elif name : user_info = self.dao.user.get_by_name(name)
        if user_info :
            self.id = user_info[0]
            self.name = user_info[1]
            self.date_of_birth = user_info[2]
            self.gender = user_info[3]
            self.email = user_info[4]
            self.password_hash = user_info[5]
            self.avatar = user_info[6]
            self.bio = user_info[7]
            self.point = user_info[8]
            self.available = user_info[9]
            self.last_active = user_info[10]
            self.create_at = user_info[11]

    def register(self, user):
        return self.dao.user.add_user(user)

    def update(self, inc_point=0):
        self.point += inc_point
        return self.dao.user.update(self)

    def set_password(self, password):
        self.password_hash =  generate_password_hash(password)
        return self.password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_last_active(self):
        self.dao.user.update_last_active(self.id, self.last_active)
        return self.last_active

    def from_last_active(self):
        days = (datetime.now() - self.last_active).days
        years = int(days/365 + 0.1)
        if years : return '{} năm trước'.format(years)
        months = int(days/31 + 0.1)
        if months : return '{} tháng trước'.format(months)
        if days : return '{} ngày trước'.format(days)
        seconds = (datetime.now() - self.last_active).seconds
        hours = int(seconds/3600 + 0.1)
        if hours : return '{} giờ trước'.format(hours)
        minutes = int(seconds/60 + 0.3)
        if minutes : return '{} phút trước'.format(minutes)
        return 'vừa xong'

    
    def get_reset_password_token(self, expires_in=300):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')
 
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User(id)

    def get_avatar_url(self):
        return '/static/image/user_avatar/{}'.format(self.avatar)

    def get_my_books(self):
        bids = self.dao.request.get_user_bids(self.id)
        books = [ Book(bid) for bid in bids ]
        return books

    def get_requesting_books(self):
        bids = self.dao.request.get_requesting_bids(self.id)
        books = [ Book(bid) for bid in bids ]
        return books
        
    def get_accepted_books(self):
        bids = self.dao.request.get_accepted_bids(self.id)
        books = [ Book(bid) for bid in bids ]
        return books

    def get_following_books(self):
        bids = self.dao.follow.get_following_bids(self.id)
        books = [ Book(bid) for bid in bids ]
        return books

    def request(self, bid):
        if self.point>0 :
            self.dao.request.request(uid=self.id, bid=bid)
            self.update(inc_point=-1)
            return True
        return False

    def cancel_request(self, bid):
        if self.dao.request.cancel_request(uid=self.id, bid=bid) :
            self.update(inc_point=1)
            return True
        return False

    def follow(self, bid):
        return self.dao.follow.follow(uid=self.id, bid=bid)

    def unfollow(self, bid):
        return self.dao.follow.unfollow(uid=self.id, bid=bid)

    def decline(self, uid, bid):
        return self.dao.request.decline_request(uid=uid, bid=bid)

    def accept(self, uid, bid):
        return self.dao.request.accept_request(uid=uid, bid=bid)

    def confirm(self, bid):
        return self.dao.request.confirm(uid=self.id, bid=bid)

    def unconfirm(self, bid):
        return self.dao.request.unconfirm(uid=self.id, bid=bid)

    def get_all_notif(self):
        return self.dao.notification.get_all_notif(self.id)

    def get_unseen_notif(self):
        return self.dao.notification.get_unseen_notif(self.id)

    def seen_notif(self, nid):
        return self.dao.notification.seen_notif(nid)

    def seen_all_notif(self):
        return self.dao.notification.seen_all_notif(self.id)

    def searchUser(self, text='', limit=7):
        return self.dao.user.searchUser(text, limit)

@login.user_loader
def load_user(id):
    return User(int(id))