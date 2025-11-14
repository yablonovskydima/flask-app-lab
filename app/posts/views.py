from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, session
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from app.posts.forms import PostForm
from app import db
from app.posts.models import Post

post_bp = Blueprint("posts", __name__, template_folder="templates")

@post_bp.route('/post/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        author = session.get("username", "Anonymous")

        post = Post(
            title=form.title.data,
            content=form.content.data,
            author=author,
            is_active=form.enabled.data,
            posted=form.posted.data,
            category=form.category.data
        )
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('posts.list_posts'))

    return render_template('posts/add_post.html', form=form)


@post_bp.route("/post")
def list_posts():
    stmt = select(Post).where(Post.is_active==True).order_by(Post.posted.desc())
    posts = db.session.scalars(stmt).all()
    return render_template("posts/post.html", posts=posts)


@post_bp.route("/post/<int:id>")
def show_post(id):
    stmt = select(Post).where(Post.id == id)
    try:
        post = db.session.scalars(stmt).one()
    except NoResultFound:
        abort(404)
    return render_template("posts/detail_post.html", post=post)


@post_bp.route("/post/<int:id>/update", methods=["GET", "POST"])
def update_post(id):
    stmt = select(Post).where(Post.id == id)
    try:
        post = db.session.scalars(stmt).one()
    except NoResultFound:
        abort(404)

    form = PostForm(obj=post)

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.enabled.data
        post.posted = form.posted.data

        db.session.commit()
        flash("Post updated successfully!", "success")
        return redirect(url_for("posts.show_post", id=post.id))

    return render_template("posts/edit_post.html", form=form, post=post)


@post_bp.route("/post/<int:id>/delete", methods=["GET", "POST"])
def delete_post(id):
    stmt = select(Post).where(Post.id == id)
    try:
        post = db.session.scalars(stmt).one()
    except NoResultFound:
        abort(404)

    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully!", "success")
        return redirect(url_for("posts.list_posts"))

    return render_template("posts/delete_confirm.html", post=post)
