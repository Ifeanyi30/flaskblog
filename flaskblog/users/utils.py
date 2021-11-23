import os
import secrets
from PIL import Image
from flask import url_for, flash, redirect, current_app
from flask_mail import Message
from flaskblog import mail


def save_picture(picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, "static/images", picture_fn)

    output_size = (125, 125)
    i = Image.open(picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    try:
        msg = Message(
            'Password Reset Request',
            sender='liamsanctus30@gmail.com',
            recipients = [user.email]
        )
        msg.body = f"""To reset your password, visit the following link:
        {url_for('users.reset_token', token=token, _external=True)}
        
        If you did not make this request then simply ignore this email and no changes
        would be made to your account.
        """
        mail.send(msg)
        flash('An email has been sent with instructions to reset your password', 'info')

    except Exception as e:
        flash('Could not send reset email token', 'danger')
        print(e)
        return redirect(url_for('users.login'))