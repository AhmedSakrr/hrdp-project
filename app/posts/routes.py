from flask import (render_template, url_for, flash
                    , redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from app import db
from app.models import Post
from app.posts.forms import PostForm

posts = Blueprint('posts', __name__)

# page에 들어갔을때 GET, 입력할때는 POST
@posts.route("/post/create", methods=['GET', 'POST'])
@login_required
def creating_post():
    # form을 form wtf을 이용한 forms.py에서 가져와 쓴다. (form은 하나의 클래스에서 가져옴)
    form = PostForm()
    # wtf의 class기반의 form을 가져와서 submit한 녀석을 validation
    print("::::creating post::::::::::::title:::::::::::", form.title.data)
    print("::::creating post::::::::::::content:::::::::", form.content.data)
    # print(":::::::", form.validate_on_submit())
    if form.validate_on_submit():
        # DB에 저장, Post from model
        print("============= inside===========")
        print(current_user)
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post created!!!', 'success')
        return redirect(url_for('main.home'))
    # rendering할때 form에다가 wtf에서 만들어낸 클래스를 기반으로 그녀석을 rendering한다.
    return render_template('post_template.html', title='New Post', form=form, legend="New Post")


# int: type (안써도 된다 - more specific하게 지정한것)
@posts.route("/post/<int:post_id>")
# @posts.route("/post/post_id")
def post(post_id):
    # get_or_404 is relative of get(), 404 is not found
    # post = Post.query.get(post_id)
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def updating_post(post_id):
    post = Post.query.get_or_404(post_id)
    # after updating the post
    if post.author != current_user:
        abort(403)  # forbidden route
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been update!', 'success')
        # redirect to detail page
        return redirect(url_for('posts.post', post_id=post_id))
    # before updating the post
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('post_template.html', title='Updating Post', form=form, legend="Update Post")


@posts.route("/post/<int:post_id>/delete", methods=['POST'])  # POST only
@login_required
def deleting_post(post_id):
    post = Post.query.get_or_404(post_id)
    # after updating the post
    if post.author != current_user:
        abort(403)  # forbidden route
    # persistent work for deletion
    db.session.delete(post)
    db.session.commit()
    flash('The post has been deleted!', 'success')
    return redirect(url_for('main.home'))