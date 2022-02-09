from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from werkzeug.urls import url_parse
from flask_login import current_user, login_required
from flask_socketio import send, emit
from app import dao, socket
from controllers.Book import Book
from controllers.Paging import Paging
from controllers.Notifications import Notifications
from controllers.Forms import *
from copy import copy
import json
import datetime

book_view = Blueprint('book_routes', __name__, template_folder='/templates')

@socket.on('message')
def handleMessage(msg):
    msg['time'] = str(datetime.datetime.now())
    send(msg, broadcast=True)

@socket.on('typing')
def handleTyping(msg):
	emit('typing', msg, broadcast=True)

@book_view.route('/')
@book_view.route('/home')
def home():
    page =  request.args.get('page', 1, type=int)
    book = Book()
    all_books = book.get_all_books()
    books = Paging(list=all_books, len_each_page=9, page=page)
    this_url = url_for('book_routes.home') + '?'

    return render_template('home.html', books=books, bookDAO=book, this_url=this_url)

@book_view.route('/new_book', methods=['GET', 'POST'])
@login_required
def new_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book()
        book.title = form.title.data
        book.author = form.author.data
        book.publishyear = str(form.publishyear.data)
        book.catalog = form.catalog.data
        book.review = form.review.data
        book.photos = []
        
        images = form.image.data
        for image in images:
            filename = book.save_photo(image)
            book.photos.append(filename)

        bid = book.add_book(current_user.id)
        current_user.update(inc_point=1)
        flash('Thêm sách mới thành công')
        return redirect(url_for('book_routes.book', bid=bid))

    return render_template('new_book.html', form=form)

@book_view.route('/book/<int:bid>/edit', methods=['GET', 'POST'])
@login_required
def edit_book(bid):
    form = BookForm()
    book = Book(bid)
    if request.method == 'GET':
        form.title.data = book.title
        form.author.data = book.author
        form.publishyear.data = book.publishyear
        form.catalog.data = book.catalog
        form.review.data = book.review

    elif form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.publishyear = str(form.publishyear.data)
        book.catalog = form.catalog.data
        book.review = form.review.data
        
        new_photos = []
        images = form.image.data
        for image in images:
            filename = book.save_photo(image)
            new_photos.append(filename)

        book.update(new_photos)
        flash('Sửa thông tin sách thành công')
        return redirect(url_for('book_routes.book', bid=book.bid))

    return render_template('edit_book.html', form=form)

@book_view.route('/book/<int:bid>', methods=['GET','POST'])
def book(bid):
    book = Book(bid)
    if request.method == 'POST':
        text = request.form.get('text').replace('<div><br></div>','').replace('&nbsp;', ' ')
        uid = request.form.get('uid')
        book.add_comment(text=text,uid=uid)

        return jsonify(None)
    else:
        Owner = User(book.uid)

        return render_template('book_view.html', book=book, Owner=Owner, dao=copy(dao))

@book_view.route('/get_comment/<int:bid>', methods=['POST'])
def get_comments(bid):
    book = Book(bid)
    result = []
    for cmt in book.get_comments():
        user = dao.user.get_by_id(cmt[1])
        avatar = user[6]
        name = user[1]
        time = str(cmt[5])
        text = cmt[3]
        result.append({'avatar':avatar, 'name':name, 'time':time, 'text':text})

    return jsonify(result)

@book_view.route('/book/<int:bid>/set_cover/<photo>')
@login_required
def set_cover(bid, photo):
    book = Book(bid)
    if book.uid == current_user.id and photo in book.photos:
        book.set_cover(photo)

    return redirect(url_for('book_routes.book', bid=bid))

@book_view.route('/book/<int:bid>/delete_photo/<photo>')
@login_required
def delete_photo(bid, photo):
    book = Book(bid)
    if book.uid == current_user.id and photo in book.photos:
        book.delete_photo(photo)

    return redirect(url_for('book_routes.book', bid=bid))

@book_view.route('/book/<int:bid>/remove_book')
@login_required
def remove_book(bid):
    book = Book(bid)
    if book.uid == current_user.id:
        book.available=0
        book.update()
        current_user.update(inc_point=-1)
        uids = book.get_requester_id(available=1)
        book.decline_all()
        notif = Notifications()
        for uid in uids:
            user = User(uid)
            user.update(inc_point=1)
            notif.removed_notif(user, book)

    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('user_routes.my_book')
        return redirect(next_page)

    return redirect(url_for('book_routes.book', bid=bid))

@book_view.route('/book/<int:bid>/post_book')
@login_required
def post_book(bid):
    book = Book(bid)
    if book.uid == current_user.id:
        book.available=1
        book.update()
        current_user.update(inc_point=1)

        uids = book.get_follower_id()

        notif = Notifications()
        for uid in uids:
            notif.available_notif(User(uid), book)

    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('user_routes.my_book')
        return redirect(next_page)

    return redirect(url_for('book_routes.book', bid=bid))

@book_view.route('/request/<int:bid>')
@login_required
def request_book(bid):
    book = Book(bid=bid)
    if current_user.id not in book.get_requester_id():
        if current_user.request(bid):
            Notifications().requested_notif(current_user, book)
            flash('Đã yêu cầu')
        else: flash('Có lỗi xảy ra hoặc không đủ điểm')
    return redirect(url_for('book_routes.book', bid=bid))

@book_view.route('/cancel_request/<int:bid>')
@login_required
def cancel_request(bid):
    if current_user.cancel_request(bid):
        flash('Đã hủy yêu cầu')
    return redirect(url_for('book_routes.book', bid=bid))

@book_view.route('/follow/<int:bid>')
@login_required
def follow(bid):
    current_user.follow(bid)
    flash('Đã theo dõi')
    return redirect(url_for('book_routes.book', bid=bid))

@book_view.route('/unfollow/<int:bid>')
@login_required
def unfollow(bid):
    current_user.unfollow(bid)
    flash('Đã bỏ theo dõi')
    return redirect(url_for('book_routes.book', bid=bid))

# search

@book_view.route('/home/search/author/<author>')
def search_by_author(author):
    page =  request.args.get('page', 1, type=int)
    book = Book()
    raw_books = book.search_by_author(author=author, limit=1000)
    books = Paging(list=raw_books, len_each_page=9, page=page)
    this_url = url_for('book_routes.search_by_author', author=author) + '?'

    return render_template('home.html', books=books, bookDAO=book, this_url=this_url)

@book_view.route('/home/search/year/<year>')
def search_by_year(year):
    page =  request.args.get('page', 1, type=int)
    book = Book()
    raw_books = book.search_by_year(year=year, limit=1000)
    books = Paging(list=raw_books, len_each_page=9, page=page)
    this_url = url_for('book_routes.search_by_year', year=year) + '?'

    return render_template('home.html', books=books, bookDAO=book, this_url=this_url)

@book_view.route('/home/search/catalog/<catalog>')
def search_by_catalog(catalog):
    page =  request.args.get('page', 1, type=int)
    book = Book()
    raw_books = book.search_by_catalog(catalog=catalog, limit=1000)
    books = Paging(list=raw_books, len_each_page=9, page=page)
    this_url = url_for('book_routes.search_by_catalog', catalog=catalog) + '?'

    return render_template('home.html', books=books, bookDAO=book, this_url=this_url)

@book_view.route("/livesearch", methods=["POST"])
def live_search():
    text = request.form.get("text")
    book = Book()
    result = book.search(text=text, limit=7)
    if len(result)<7:
        books = book.search_by_author(author=text, limit=7-len(result))
        temp = []
        for x in books:
            title = '<b>Tác giả ' + x[2] + ': </b>' + x[1]
            temp += [(x[0], title)]
        result += temp
    if len(result)<7:
        books = book.search_by_year(year=text, limit=7-len(result))
        temp = []
        for x in books:
            title = '<b>Năm ' + str(x[3]) + ': </b>' + x[1]
            temp += [(x[0], title)]
        result += temp

    return jsonify(result)

@book_view.route('/home/search')
def search():
    text =  request.args.get('text', None, type=str)
    page =  request.args.get('page', 1, type=int)
    book = Book()
    raw1_books = book.search(text=text, limit=1000)
    raw2_books = book.search_by_author(author=text, limit=1000)
    raw3_books = book.search_by_year(year=text, limit=1000)
    books = Paging(list=raw1_books+raw2_books+raw3_books, len_each_page=9, page=page)
    this_url = url_for('book_routes.search', text=text) + '&'

    return render_template('home.html', books=books, bookDAO=book, this_url=this_url)

