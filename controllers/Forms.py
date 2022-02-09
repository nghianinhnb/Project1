from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, SelectField, TextAreaField, FileField, IntegerField, MultipleFileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional, Length, Regexp, InputRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from controllers.User import User
from flask_login import current_user


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Mục này không được bỏ trống'),
                                                Email(message='Email không hợp lệ')])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    remember_me = BooleanField('Duy trì đăng nhập')
    submit = SubmitField('Đăng nhập')


class RegistrationForm(FlaskForm):
    name = StringField('Tên người dùng', validators=[DataRequired(message='Mục này không được bỏ trống')])
    date_of_birth = DateField('Ngày sinh', format='%Y-%m-%d', validators=[DataRequired(message='Mục này không được bỏ trống')])
    gender = SelectField('Giới tính', choices=[('nam','nam'), ('nữ','nữ'), ('khác','khác')], validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(message='Mục này không được bỏ trống'), 
                                                Email(message='Email không hợp lệ')])
    password = PasswordField('Mật Khẩu', validators=[DataRequired(message='Mục này không được bỏ trống')])
    password2 = PasswordField(
        'Gõ lại mật khẩu', validators=[DataRequired(message='Mục này không được bỏ trống'), 
                                       EqualTo('password', message='Gõ lại không chính xác')])
    submit = SubmitField('Đăng ký')
 
    def validate_name(self, name):
        user = User(name=name.data)
        if user.id is not None:
            raise ValidationError('Tên người dùng đã được sử dụng')

    def validate_email(self, email):
        user = User(email=email.data)
        if user.id is not None:
            raise ValidationError('Email đã được sử dụng')

    def validate_password(self, password):
        if len(password.data) < 6 or password.data.find(' ') > -1:
            raise ValidationError('Mật khẩu phải gồm ít nhất 6 ký tự và không chứa khoảng trắng')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Mục này không được bỏ trống'), 
                                             Email(message='Email không hợp lệ')])
    submit = SubmitField('Lấy lại mật khẩu')

    def validate_email(self, email):
        user = User(email=email.data)
        if user.id is None:
            raise ValidationError('Không có tài khoản với email này')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Mật khẩu', validators=[DataRequired(message='Mục này không được bỏ trống')])
    password2 = PasswordField(
        'Gõ lại mật khẩu', validators=[DataRequired(message='Mục này không được bỏ trống'),
                                      EqualTo('password', message='Gõ lại không chính xác')])
    submit = SubmitField('Đặt lại mật khẩu')

    def validate_password(self, password):
        if len(password.data) < 6 or password.data.find(' ') > -1:
            raise ValidationError('Mật khẩu phải gồm ít nhất 6 ký tự và không chứa khoảng trắng')

class EditProfileForm(FlaskForm):
    name = StringField('Họ & Tên',validators=[Optional()])
    date_of_birth = DateField('Ngày sinh', format='%Y-%m-%d', validators=[Optional()])
    gender = SelectField('Giới tính', choices=[('nam','nam'), ('nữ','nữ'), ('khác','khác')], validators=[Optional()])
    bio = TextAreaField('Bio', validators=[Optional(), 
                        Length(max=400, message='Bio không được quá 400 kí tự')])
    submit1 = SubmitField('Lưu thay đổi')

    def validate_name(self, name):
        user = User(name=name.data)
        if user.id is not None and user.id != current_user.id:
            raise ValidationError('Tên người dùng đã được sử dụng')

class UploadAvatarForm(FlaskForm):
    image = FileField('image', validators=[FileAllowed(["png", "jpg", "jpeg"], "Ảnh không đúng định dạng !")])
    submit2 = SubmitField('Tải ảnh lên')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Mật khẩu cũ', validators=[DataRequired(message='Mục này không được bỏ trống')])
    new_password = PasswordField('Mật khẩu mới', validators=[DataRequired(message='Mục này không được bỏ trống')])
    new_password2 = PasswordField('Gõ lại mật khẩu mới', validators=[DataRequired(message='Mục này không được bỏ trống'),
                                                                     EqualTo('new_password', message='Gõ lại không chính xác')])
    submit = SubmitField('Lưu thay đổi')

    def validate_old_password(self, old_password):
        if not current_user.check_password(old_password.data):
            raise ValidationError('Mật khẩu không đúng')

    def validate_new_password(self, new_password):
        if len(new_password.data) < 6 or new_password.data.find(' ') > -1:
            raise ValidationError('Mật khẩu phải gồm ít nhất 6 ký tự và không chứa khoảng trắng')

class BookForm(FlaskForm):
    choices = [('Thể loại', 'Thể loại'), ('Văn học','Văn học'), ('Kinh tế','Kinh tế'), ('Tâm lý - kỹ năng sống','Tâm lý - kỹ năng sống'), 
               ('Truyện - sách thiếu nhi','Truyện - sách thiếu nhi'), ('Tiểu sử - hồi ký','Tiểu sử - hồi ký'), 
               ('Giáo khoa - giáo trình - tham khảo','Giáo khoa - giáo trình - tham khảo'), 
               ('Sách nước ngoài','Sách nước ngoài')]
    title = StringField('Tên sách', validators=[DataRequired(message='Mục này không được bỏ trống')])
    author = StringField('Tác giả', validators=[Optional()])
    publishyear = IntegerField('Năm xuất bản', validators=[DataRequired()])
    catalog = SelectField('Thể loại', choices=choices, validators=[DataRequired()])
    review = TextAreaField('Giới thiệu', validators=[Optional(), 
                                                     Length(max=500, message='Phần giới thiệu không được quá 500 kí tự')])
    image = MultipleFileField('image', validators=[FileAllowed(["png", "jpg", "jpeg"], "Ảnh không đúng định dạng !")])

    submit = SubmitField('Đăng sách')

    def validate_publishyear(self, publishyear):
        if int(publishyear.data)<1000 or int(publishyear.data)>2100 :
            raise ValidationError('Năm xuất bản phải sau năm 1000 và trước năm 2100')

    def validate_catalog(self, catalog):
        if catalog.data == 'Thể loại':
            raise ValidationError('Hãy chọn thể loại')

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[Length(max=1000, message='Bình luận không được quá 1000 kí tự')])
    submit = SubmitField('Gửi')