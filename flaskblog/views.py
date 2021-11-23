import os
import secrets
from PIL import Image
from flaskblog import app, bcrypt, db, mail
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from flaskblog.model import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from is_safe_url import is_safe_url
from flask_mail import Message








    






if __name__ == "__main__":
    app.run(debug=True)
