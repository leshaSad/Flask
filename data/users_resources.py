from flask import jsonify
from flask_restful import Resource, abort
from werkzeug.security import generate_password_hash
from . import db_session


def abort_if_news_not_found(news_id):
    session = db_session.create_session()
    news = session.query(News).get(news_id)
    if not news:
        abort(404, message=f"News {news_id} not found")