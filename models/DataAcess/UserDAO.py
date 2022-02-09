import datetime

class UserDAO:
    def __init__(self, DAO):
        self.db = DAO
        self.db.table = 'user'

    # Thêm
    def add_user(self, user):
        name = user.name 
        date_of_birth = user.date_of_birth
        gender = user.gender 
        email = user.email
        password_hash = user.password_hash

        q = self.db.query("INSERT INTO user (`name`, `date_of_birth`, `gender`, `email`, `password_hash`) VALUES ('{}', '{}', '{}', '{}', '{}')"
                          .format(name, date_of_birth, gender, email, password_hash))
        self.db.commit()

        return name

    # Đọc
    def get_by_id(self, uid):
        if uid:
            q = self.db.query('select * from @table where uid={}'.format(uid))
            user = q.fetchone()
            return user
        return None

    def get_by_email(self, email):
        q = self.db.query("select * from @table where email='{}'".format(email))
        user = q.fetchone()

        return user

    def get_by_name(self, name):
        q = self.db.query("select * from @table where name='{}'".format(name))
        user = q.fetchone()

        return user

    def searchUser(self, text='', limit=7):
        q = self.db.query("select * from @table where name LIKE '%{}%' \
                            or match(name) against('{}' WITH QUERY EXPANSION) limit {};"
                            .format(text, text, limit))
        users = q.fetchall()

        return users

    # Sửa
    def update(self, user):
        uid = user.id
        name = user.name
        date_of_birth = user.date_of_birth
        gender = user.gender
        password_hash = user.password_hash
        avatar = user.avatar
        bio = user.bio
        point = user.point
        available = user.available

        q = self.db.query("UPDATE @table SET name='{}', date_of_birth='{}', gender='{}', password_hash='{}', avatar='{}', bio='{}', point={}, available={}, modify_at='{}' WHERE uid={}"
                          .format(name, date_of_birth, gender, password_hash, avatar, bio, point, available, datetime.datetime.now(), uid))
        self.db.commit()

        return q

    def update_last_active(self, uid, datetime):
         q = self.db.query("UPDATE @table SET last_active='{}' WHERE uid={}".format(datetime, uid))
         self.db.commit()
         
         return q
