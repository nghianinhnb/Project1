from flask import Blueprint, render_template, flash, redirect, url_for, request, send_from_directory, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.urls import url_parse
from controllers.Forms import *
from app import login, socket, app, avatars
from controllers.User import User
from controllers.Book import Book
from datetime import datetime
from controllers.Email import send_password_reset_email
from controllers.Paging import Paging
from controllers.Time import Time
from controllers.Notifications import Notifications
from os import path, remove
import json

user_view = Blueprint('user_routes', __name__, template_folder='/templates')
time = Time()



@user_view.route('/heart_beat', methods=['POST'])
def heart_beat():
    uid = request.form.get('uid')
    time.heart_beat(uid)
    return jsonify(None)

@user_view.route('/get_status', methods=['POST'])
def get_status():
    uid = request.form.get('uid')
    result = {}
    result['status'] = time.get_status(uid)
    if result['status'] == 'Đang hoạt động':
        result['dot'] = '<i class="fas fa-circle"></i>'
    else: result['dot'] = '<i class="far fa-circle"></i>'
    return jsonify(result)

@user_view.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('book_routes.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        if user.id is None or not user.check_password(form.password.data):
            flash('Email hoặc mật khẩu không đúng')
            return redirect(url_for('user_routes.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('book_routes.home')
        return redirect(next_page)
    return render_template('login.html', form=form)


@user_view.route('/logout')
def logout():
    current_user.last_active = datetime.now()
    current_user.update_last_active()
    logout_user()
    return redirect(url_for('book_routes.home'))


@user_view.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('book_routes.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()

        user.name = form.name.data
        user.date_of_birth = form.date_of_birth.data
        user.gender = form.gender.data
        user.email = form.email.data
        user.set_password(form.password.data)

        user.register(user)
        flash('Đăng ký thành công')
        return redirect(url_for('user_routes.login'))
    return render_template('register.html', form=form)


@user_view.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('book_routes.home'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        if user.id :
            send_password_reset_email(user)
        flash('Kiểm tra email để khôi phục mật khẩu, nhớ kiểm tra phần thư spam nếu không thấy nhé!')
        return redirect(url_for('user_routes.login'))
    return render_template('reset_password_request.html', form=form)

@user_view.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('book_routes.home'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('book_routes.home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.update()
        flash('Đặt lại mật khẩu thành công')
        return redirect(url_for('user_routes.login'))
    return render_template('reset_password.html', form=form)


@user_view.route('/account/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    upload_avatar = UploadAvatarForm()
    if request.method == 'GET':
        form.name.data = current_user.name
        form.date_of_birth.data = current_user.date_of_birth
        form.gender.data = current_user.gender
        form.bio.data = current_user.bio
    else: 
        if form.submit1.data and form.validate():
            current_user.name = form.name.data
            current_user.date_of_birth = form.date_of_birth.data
            current_user.gender = form.gender.data
            current_user.bio = form.bio.data
            current_user.update()

        if upload_avatar.submit2.data and upload_avatar.validate():
            f = upload_avatar.image.data
            if f:
                raw_filename = avatars.save_avatar(f)
                if path.exists(app.config['AVATARS_SAVE_PATH'] + current_user.avatar):
                    remove(app.config['AVATARS_SAVE_PATH'] + current_user.avatar)
                current_user.avatar = raw_filename
                current_user.update()
            return redirect(url_for('user_routes.crop_avatar'))

        flash('Cập nhật thông tin tài khoản thành công')
        return redirect(url_for('user_routes.edit_profile'))
    return render_template('edit_profile.html', form=form, upload_avatar=upload_avatar)

@app.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(app.config['AVATARS_SAVE_PATH'], filename)

@user_view.route('/account/crop_avatar', methods=['GET', 'POST'])
@login_required
def crop_avatar():
    if request.method == 'POST':
        x = request.form.get('x')
        y = request.form.get('y')
        w = request.form.get('w')
        h = request.form.get('h')
        filename = avatars.crop_avatar(current_user.avatar, x, y, w, h)
        if path.exists(app.config['AVATARS_SAVE_PATH'] + current_user.avatar):
            remove(app.config['AVATARS_SAVE_PATH'] + current_user.avatar)
        current_user.avatar = filename
        current_user.update()
        return redirect(url_for('user_routes.edit_profile'))
    return render_template('crop_avatar.html')


@user_view.route('/account/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.new_password.data)
        current_user.update()
        flash('Đổi mật khẩu thành công')
        return redirect(url_for('user_routes.edit_profile'))
    return render_template('change_password.html', form=form)

@user_view.route('/account/deactive_account')
@login_required
def deactive_account():
    
    return redirect(url_for('book_routes.home'))

@user_view.route('/account/my_book')
@login_required
def my_book():
    page = request.args.get('page', 1, type=int)
    my_book = current_user.get_my_books()
    length = len(my_book)
    books = Paging(list=my_book, len_each_page=3 , page=page)

    return render_template('my_book.html', books=books, len=length)

@user_view.route('/account/notification', methods=['GET', 'POST'])
@login_required
def notification():

    return render_template('notification.html')

@user_view.route('/account/following_book', methods=['GET', 'POST'])
@login_required
def following():
    page = request.args.get('page', 1, type=int)
    following_books = current_user.get_following_books()
    length = len(following_books)
    books = Paging(list=following_books, len_each_page=5 , page=page)

    return render_template('following_book.html', books=books, len=length)

@user_view.route('/account/requesting_book', methods=['GET', 'POST'])
@login_required
def requesting():
    page = request.args.get('page', 1, type=int)
    accepted_books = current_user.get_accepted_books()
    requesting_books = current_user.get_requesting_books()
    length = len(requesting_books)
    books = Paging(list=accepted_books+requesting_books, len_each_page=5 , page=page)

    return render_template('requesting_book.html', books=books, len=length)

@user_view.route('/user/<int:uid>')
def user(uid):
    return 'user ' + str(uid)

@user_view.route('/accept/<int:uid>/<int:bid>')
@login_required
def accept(uid,bid):
    book = Book(bid)
    if (book.uid == current_user.id):
        current_user.accept(uid, bid)
        notif = Notifications()
        notif.accept_notif(User(uid), book)
        
    return redirect(url_for('user_routes.my_book'))

@user_view.route('/decline/<int:uid>/<int:bid>')
@login_required
def decline(uid,bid):
    book = Book(bid)
    if (book.uid == current_user.id):
        current_user.decline(uid, bid)
        User(uid).update(inc_point=1)
        notif = Notifications()
        notif.decline_notif(User(uid), book)
        
    return redirect(url_for('user_routes.my_book'))

@user_view.route('/confirm/<int:bid>')
@login_required
def confirm(bid):
    book = Book(bid)
    book.available = 0
    book.update()
    uids = book.get_requester_id(available=1)
    book.decline_all()
    current_user.confirm(bid)
    notif = Notifications()
    notif.confirm_notif(currnet_user, book)
    for uid in uids:
        user = User(uid)
        user.update(inc_point=1)
        notif.taken_notif(user,book)
        
    return redirect(url_for('user_routes.my_book'))

@user_view.route('/unconfirm/<int:bid>')
@login_required
def unconfirm(bid):
    book = Book(bid)
    current_user.update(inc_point=1)
    current_user.unconfirm(bid)
    notif = Notifications()
    notif.unconfirm_notif(current_user, book)
        
    return redirect(url_for('user_routes.my_book'))

@user_view.route("/tag", methods=["POST"])
@login_required
def tag():
    try:
        _text = request.form.get("text")
        user = User()
        _text = _text.split('@')
        _list = user.searchUser(text=_text[1], limit=7)
        result = {'text':_text[0], 'list':_list}

        return jsonify(result)
    except:
        return jsonify(None)

@user_view.route("/tagged_notif", methods=["POST"])
def tagged_notif():
    name = request.form.get("name")
    bid = request.form.get("bid")
    notif = Notifications()
    notif.tagged_notif(User(name=name), Book(bid=bid))

    return jsonify(None)

@user_view.route("/get_notification", methods=["POST"])
def get_notification():
    uid = request.form.get("uid")
    user = User(id=uid)
    result = user.get_all_notif()

    return jsonify(result)

@user_view.route("/seen", methods=["POST"])
def seen():
    nid = request.form.get("nid")
    Notifications().seen(nid)

    return jsonify(None)

@user_view.route("/get_num_unseen_notif", methods=["POST"])
def get_num_unseen_notif():
    uid = request.form.get("uid")
    unseen_notif = User(id=uid).get_unseen_notif()
    num = len(unseen_notif)
    if num>0:
        return jsonify(num)
    else: return jsonify(None)