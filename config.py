import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = 'KhOa-bI-MaT'
    HOST = "localhost"
    USER = "nghia"
    PASSWORD = ""
    DATABASE = "project1"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'BoookVN'
    MAIL_PASSWORD = '12345sau'
    ADMINS = ['BoookVN@gmail.com']
    AVATARS_SAVE_PATH = basedir + '\\static\\image\\user_avatar\\'
    PHOTOS_SAVE_PATH = basedir + '\\static\\image\\book_photos\\'