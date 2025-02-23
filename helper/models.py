from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    karma = Column(Integer, nullable=False)
    created = Column(DateTime, nullable=True)

    posts = relationship('Post', back_populates='author')

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    submission_id = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    subreddit_id = Column(Integer, ForeignKey('subreddits.id'), nullable=False)
    is_self = Column(Boolean, nullable=False)
    is_original_content = Column(Boolean, nullable=False)
    text = Column(String)
    flair = Column(String)

    ratings = relationship('SubmissionRating', back_populates='post')
    author = relationship('Author', back_populates='posts')
    subreddit = relationship('Subreddit', back_populates='posts')

class SubmissionRating(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True)
    num_comments = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    upvote_ratio = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)

    post = relationship('Post', back_populates='ratings')

class Subreddit(Base):
    __tablename__ = 'subreddits'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    posts = relationship('Post', back_populates='subreddit')
    members = relationship('Member', back_populates='subreddit')

class Member(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)
    subreddit_id = Column(Integer, ForeignKey('subreddits.id'), nullable=False)
    members_count = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    
    subreddit = relationship('Subreddit', back_populates='members')

