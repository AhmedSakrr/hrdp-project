import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from app import mail

# saving profile pic in server file system
def saving_pic(form_picture):
    # secret import for random pic file name
    random_hex = secrets.token_hex(8)
    # in order to get file extension, os import, and splitext func return two values
    _, file_ext = os.path.splitext(form_picture.filename)  # when using only on value, the other one should be _
    # making new file name
    new_picture_filename = random_hex + file_ext
    # making path to store new pic
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', new_picture_filename)
    print("::::::::::::::::::", picture_path)
    # before saving the pic, resizing using PIL import Image
    pixel_size = (122, 122)
    resized_image = Image.open(form_picture)
    resized_image.thumbnail(pixel_size)
    # saving new picture in the path
    resized_image.save(picture_path)

    return new_picture_filename


# flask-mail package 이용
def sending_reset_email(user):

    # default 3600
    token = user.getting_token()

    # Message(subject, sender, recipient)
    message = Message('Password Reset Request', sender='attobes@gmail.com', recipients=[user.email])

    # external: using this for absolute path, relative is just for the app here.
    message.body = f'''In order to reset your password, Visit the link below:

{url_for('users.resetting_password', token=token, _external=True)}
If you did not make this request, call us immediately or change your password.
'''
    print(message)
    mail.send(message)
