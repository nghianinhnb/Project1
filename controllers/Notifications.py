from app import dao as DAO
from copy import copy
from flask import url_for

class Notifications:
    def __init__(self):
        self.dao = copy(DAO)

    
    def seen(self, nid):
        self.dao.notification.seen_notif(nid)

# thong bao da dong y
    def accept_notif(self, user, book):
        text = 'Bạn đã được đồng ý lấy quyển <a href="{}">{}<a> hãy xác nhận đồng ý và chủ sở hữu sẽ chuyển sách cho bạn. Lưu ý yêu cầu lấy\
        sẽ được tự động xác nhận trong 1 ngày tính từ khi bạn nhận được thông báo này'\
        .format(url_for('book_routes.book', bid=book.bid), book.title)
        return self.dao.notification.make_notif(user.id, text)

# thong bao da tu choi
    def decline_notif(self, user, book):
        text = 'Bạn đã không được đồng ý lấy quyển <a href="{}">{}<a>. Điểm sẽ được cộng lại cho bạn'\
        .format(url_for('book_routes.book', bid=book.bid), book.title)
        return self.dao.notification.make_notif(user.id, text)

# thong bao da xac nhan
    def confirm_notif(self, user, book):
        text = '<a href="">{}</a> đã xác nhận lấy quyển <a href="{}">{}</a>, hãy bắt đầu gửi sách cho họ'\
        .format(user.name, url_for('book_routes.book', bid=book.bid), book.title)
        return self.dao.notification.make_notif(book.uid, text)

# thong bao khong xac nhan
    def unconfirm_notif(self, user, book):
        text = '<a href="">{}</a> đã không xác nhận lấy quyển <a href="{}">{}</a>, hãy xem xét các yêu cầu lấy còn lại'\
            .format(user.name, url_for('book_routes.book', bid=book.bid), book.title)
        return self.dao.notification.make_notif(book.uid, text)

# thong bao sach da go
    def removed_notif(self, user, book):
        text = 'Quyển <a href="{}">{}</a> mà bạn yêu cầu đã bị gỡ, điểm đã được cộng lại cho bạn'\
            .format(url_for('book_routes.book', bid=book.bid), book.title)
        return self.dao.notification.make_notif(user.id, text)

# thong bao sa cho nguoi khac lay
    def taken_notif(self, user, book):
        text = 'Quyển <a href="{}">{}</a> mà bạn yêu cầu đã cho người khác lấy, điểm đã được cộng lại cho bạn'\
            .format(url_for('book_routes.book', bid=book.bid), book.title)
        return self.dao.notification.make_notif(user.id, text)

# thong bao sach ban muon da co the yeu cau lay
    def available_notif(self, user, book):
        text = 'Quyển <a href="{}">{}</a> mà bạn theo dõi đã được đăng. Bây giờ, bạn có thể yêu cầu lấy'\
            .format(url_for('book_routes.book', bid=book.bid), book.title)
        return self.dao.notification.make_notif(user.id, text)

# thong bao co nguoi yeu cau muon
    def requested_notif(self, user, book):
        text = '<a href="">{}</a> đã yêu cầu lấy quyển <a href="{}">{}</a>'\
            .format(user.name, url_for('book_routes.book', bid=book.bid), book.title)
        return self.dao.notification.make_notif(book.uid, text)

    def tagged_notif(self, user, book):
        text = 'Bạn đã được nhắc đến trong một <a href="{}">bình luận</a>'\
            .format(url_for('book_routes.book', bid=book.bid))
        return self.dao.notification.make_notif(user.id, text)