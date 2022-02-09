from copy import copy

from models.DB import DB

from models.DataAcess.BookDAO import BookDAO
from models.DataAcess.UserDAO import UserDAO
from models.DataAcess.RequestDAO import RequestDAO
from models.DataAcess.FollowDAO import FollowDAO
from models.DataAcess.PhotoDAO import PhotoDAO
from models.DataAcess.CommentDAO import CommentDAO
from models.DataAcess.NotificationDAO import NotificationDAO


class DAO(DB):
    def __init__(self, app):
        super(DAO, self).__init__(app)

        self.book = BookDAO(copy(self))
        self.user = UserDAO(copy(self))
        self.request = RequestDAO(copy(self))
        self.follow = FollowDAO(copy(self))
        self.photo = PhotoDAO(copy(self))
        self.comment = CommentDAO(copy(self))
        self.notification = NotificationDAO(copy(self))