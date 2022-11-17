from flask import Blueprint,render_template, request, flash, redirect, url_for, abort
from flask_login import login_required,current_user
from .models import Post, User, Comment
from website._init_ import db
from website import comm
from website.forms import CommunityForm


views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template ("home.html", user=current_user, posts=posts)

@views.route("/community/<string:name>")
def community(name):
    """
    Route for page displaying a community and its posts sorted by date created.
    """
    page = int(request.args.get("page", 1))
    community = comm.get_community(name)
    if community:
        posts = comm.get_community_posts(community.id, page, False)
        community_member = None
        if current_user.is_authenticated:
            community_member = comm.get_community_member(
                community.id, current_user.id
            )
        return render_template(
            "community.html",
            tab="recent",
            community=community,
            posts=posts,
            community_member=community_member,
        )
    else:
        abort(404)

@views.route("/community/<string:name>/top")
def top_community(name):
    """
    Route for page displaying a community and its posts sorted by number of upvotes.
    """
    page = int(request.args.get("page", 1))
    community = comm.get_community(name)
    if community:
        posts = comm.get_community_posts(community.id, page, True)
        community_member = None
        if current_user.is_authenticated:
            community_member = comm.get_community_member(
                community.id, current_user.id
            )
        return render_template(
            "community.html",
            tab="top",
            community=community,
            posts=posts,
            community_member=community_member,
        )
    else:
        abort(404)

@views.route("/community/create", methods=["GET", "POST"])
@login_required
def create_community():
    """
    Route for creating a community. On a GET request, it returns the community creation
    form. On a POST request, it processes a community creation.
    """
    form = CommunityForm()
    if form.validate_on_submit():
        comm.create_community(
            form.name.data, form.description.data, current_user
        )
        flash("Successfully created community.", "primary")
        return redirect(url_for("community.community", name=form.name.data))
    return render_template("create_community.html", form=form)

@views.route("/createpost", methods=['GET','POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('createpost.html', user=current_user)

@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted', category='success')

    comment = Comment.query.filter(Comment.post_id == id).all()
    if not comment:
        pass
    else:
        for c in comment:
            db.session.delete(c)
        db.session.commit()


    return redirect(url_for('views.home'))

@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists', category='error')
        return redirect(url_for('views.home'))

    posts = user.posts
    return render_template("posts.html", user=current_user, posts=posts, username=username)

@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist', category='error')

    return redirect(url_for('views.home'))

@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home'))