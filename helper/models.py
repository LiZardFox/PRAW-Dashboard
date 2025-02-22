from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Author(Base):
    __tablename__ = 'authors'
    name = Column(String, primary_key=True, nullable=False)

    posts = relationship('Post', back_populates='author')

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    upvote_ratio = Column(Float, nullable=False)
    author_name = Column(Integer, ForeignKey('authors.name'), nullable=False)
    num_comments = Column(Integer, nullable=False)
    is_self = Column(Boolean, nullable=False)
    is_original_content = Column(Boolean, nullable=False)
    score_member_ratio = Column(Float, nullable=False)
    text = Column(String)
    flair = Column(String)

    author = relationship('Author', back_populates='posts')
