from website._init_ import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import datetime

class User(db.Model, UserMixin):
    """Model that represents a user."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    communities = db.relationship("Community", backref="app_user", lazy="dynamic", cascade="all, delete-orphan")
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    likes = db.relationship('Like', backref='user', passive_deletes=True)
    post_votes = db.relationship(
        "PostVote", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )
    reply_votes = db.relationship(
        "ReplyVote", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )
    community_members = db.relationship(
        "CommunityMember",
        backref="user",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<AppUser (id='{self.id}', username='{self.username}')>"

class Community(db.Model):
    """Model that represents a community."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    posts = db.relationship(
        "Post", backref="community", lazy="dynamic", cascade="all, delete-orphan"
    )
    community_members = db.relationship(
        "CommunityMember",
        backref="community",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Community (id='{self.id}', name='{self.name}', description='{self.description}', date_created='{self.date_created}')>"


class Post(db.Model):
    """Model that represents a post."""

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text,nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey("community.id"), nullable=False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    likes = db.relationship('Like', backref='post', passive_deletes=True)
    post_votes = db.relationship(
        "PostVote", backref="post", lazy="dynamic", cascade="all, delete-orphan"
    )

class Comment(db.Model):
    """Model that represents a user's comment."""

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow
    )
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)
    reply_votes = db.relationship(
        "ReplyVote", backref="reply", lazy="dynamic", cascade="all, delete-orphan"
    )

class Like(db.Model):
    """Model that tracks a user's likes on a comment."""
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)

class PostVote(db.Model):
    """Model that tracks a user's vote on a post."""

    id = db.Column(db.Integer, primary_key=True)
    vote = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

    def __repr__(self):
        return f"<PostVote (id='{self.id}', vote='{self.vote}')>"


class ReplyVote(db.Model):
    """Model that tracks a user's vote on a reply."""

    id = db.Column(db.Integer, primary_key=True)
    vote = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    reply_id = db.Column(db.Integer, db.ForeignKey("comment.id"), nullable=False)

    def __repr__(self):
        return f"<ReplyVote (id='{self.id}', vote='{self.vote}')>"


class CommunityMember(db.Model):
    """Model that tracks a user's community membership."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey("community.id"), nullable=False)

    def __repr__(self):
        return f"<CommunityMember (id='{self.id}')>"