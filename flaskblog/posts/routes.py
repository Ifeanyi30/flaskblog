from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.model import Post
from flaskblog.posts.forms import PostForm



posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created", "success")
        return redirect(url_for("main.home"))
    return render_template("create_post.html", title="New Post", form=form)
 
@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    t_len = len(post.title)
    c_len = len(post.content)
    if form.validate_on_submit():
        if len(form.content.data) != c_len or len(form.title.data) == t_len:
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash("your blog has been updated!", "success")
            return redirect(url_for("posts.post", post_id=post.id))
        else:
            flash('You did not edit your post', 'info')
            return redirect(url_for("posts.post", post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content    
    return render_template("update_post.html", title="Update Post", form=form)


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("your blog has been deleted", "success")
    return redirect(url_for('main.home'))