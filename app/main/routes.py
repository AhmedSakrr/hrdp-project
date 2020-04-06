from flask import render_template, request, Blueprint
from app.models import Post

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    # retrieving posts from db using the Post model
    # page retrieving from request, page arg name, default val = 1, val constraint = int
    page = request.args.get('page', 1, type=int)
    # legacy -> pagination
    # order: order_by(Post.date_posted.desc())
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)

    return render_template('home.html', title='home', posts=posts)


@main.route('/about')
def about():
    return render_template('about.html', title='About')
