from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app import db
from app.posts.models import Post

post_bp = Blueprint("posts", __name__, template_folder="templates")

@post_bp.route("/post/create", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        category = request.form.get("category", "OTHER").upper()
        author = request.form.get("author", "Anonymous")
        is_active = request.form.get("is_active", True)

        post = Post(
            title=title,
            content=content,
            category=category,
            author=author,
            is_active=bool(is_active)
        )
        db.session.add(post)
        db.session.commit()
        flash("Post created successfully!", "success")
        return redirect(url_for("posts.list_posts"))

    return render_template("posts/add_post.html")


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

    if request.method == "POST":
        post.title = request.form.get("title", post.title)
        post.content = request.form.get("content", post.content)
        post.category = request.form.get("category", post.category)
        post.author = request.form.get("author", post.author)
        post.is_active = bool(request.form.get("is_active"))

        db.session.commit()
        flash("Post updated successfully!", "success")
        return redirect(url_for("posts.show_post", id=post.id))

    return render_template("posts/edit_post.html", post=post)


@post_bp.route("/post/<int:id>/delete", methods=["POST"])
def delete_post(id):
    stmt = select(Post).where(Post.id == id)
    try:
        post = db.session.scalars(stmt).one()
    except NoResultFound:
        abort(404)

    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully!", "success")
    return redirect(url_for("posts.list_posts"))
