import sqlalchemy as sa
import sqlalchemy.orm as so

from app import db, login, prediction_model
from typing import Optional
from sqlalchemy.ext.mutable import MutableList
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


MAX_LIKED_TRACKS_SIZE = 100  # todo change to 1000


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(256), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    liked_tracks_ids: so.Mapped[list[int]] = (
        so.mapped_column(MutableList.as_mutable(sa.PickleType),
                         default=[]))
    genres: so.Mapped[list[str]] = (
        so.mapped_column(MutableList.as_mutable(sa.PickleType),
                         default=[]))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_liked_tracks(self, new_liked_tracks, replace=False):
        if replace:
            self.liked_tracks_ids.clear()
        self.liked_tracks_ids.extend(new_liked_tracks)
        db.session.add(self)
        db.session.commit()
        if len(self.liked_tracks_ids) > MAX_LIKED_TRACKS_SIZE:
            self.liked_tracks_ids = self.liked_tracks_ids[len(self.liked_tracks_ids) - MAX_LIKED_TRACKS_SIZE:]

    def get_liked_tracks(self):
        data = prediction_model.initial_data.iloc[self.liked_tracks_ids]
        indexes = data.index.values.tolist()
        res = data[['full_title']].values.tolist()
        return [(indexes[idx], res[idx][0]) for idx in range(len(indexes))]

    def set_genres(self, genres):
        self.genres = genres

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
