"""The entry point for flask app"""

import os
import random
import flask
import flask_login

from wikipedia import get_wiki_link
from tmdb import get_movie_data

from app_factory import app, db, login_manager
from bussiness_dao import User, Review
import login_util

db.create_all()
login_manager.init_app(app)

# MOVIE_IDS = ["127380", "508947", "277834"]
MOVIE_IDS = ["127380"]


@app.route("/")
@flask_login.login_required
def index():
    """The index page

    Returns:
        html: html string
    """
    movie_id = random.choice(MOVIE_IDS)

    # API calls
    (title, tagline, genre, poster_image) = get_movie_data(movie_id)
    wikipedia_url = get_wiki_link(title)

    review_iter = Review.query.filter_by(movie_id=movie_id)
    review_list = []
    if review_iter is not None:
        review_list = list(review_iter)

    return flask.render_template(
        "index.html",
        title=title,
        tagline=tagline,
        genre=genre,
        poster_image=poster_image,
        wiki_url=wikipedia_url,
        review_list=review_list,
        movie_id=movie_id,
    )


@app.route("/submitReview", methods=["POST"])
def submit_review():
    """submit review controller

    Returns:
        _type_: html response
    """
    username = User.query.filter_by(id=flask_login.current_user.id).first().username
    comment = flask.request.form["comment"]
    rate = flask.request.form["rating"]
    movie_id = flask.request.form["movie_id"]
    db.session.add(
        Review(username=username, comment=comment, rate=rate, movie_id=movie_id)
    )
    db.session.commit()
    return flask.redirect(flask.url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """login controller

    Returns:
        _type_: html response
    """
    if flask.request.method == "GET":
        return flask.render_template("login.html")
    else:
        username = flask.request.form["username"]
        password = flask.request.form["password"]
        quried_user = User.query.filter_by(username=username).first()
        if quried_user is None or quried_user.password != password:
            return flask.redirect(flask.url_for("login"))
        else:
            flask_login.login_user(quried_user)
            return flask.redirect(flask.url_for("index"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """signup controller

    Returns:
        _type_: html response
    """
    if flask.request.method == "GET":
        return flask.render_template("signup.html")
    elif flask.request.method == "POST":
        username = flask.request.form["username"]
        password = flask.request.form["password"]
        # save username to database
        if User.query.filter_by(username=username).first() is None:
            db.session.add(User(username=username, password=password))
            db.session.commit()
        return flask.redirect(flask.url_for("login"))


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True
    )
