from controllers.User import User
import datetime

class Time:
    timeout = 6

    def __init__(self):
        self.last_active = {}

    def heart_beat(self, uid):
        self.last_active[uid] = datetime.datetime.now()

    def get_status(self, uid):
        if uid in self.last_active:
            if (datetime.datetime.now() - self.last_active[uid]).seconds < self.timeout:
                return 'Đang hoạt động'
            else: 
                user = User(uid)
                user.last_active = self.last_active[uid]
                user.update_last_active()
                return 'Hoạt động ' + user.from_last_active()
        return 'Hoạt động ' + User(uid).from_last_active()