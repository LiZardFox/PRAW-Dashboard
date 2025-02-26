import praw
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from helper.models import Base, Author, Post, Subreddit, Member, SubmissionRating
from datetime import datetime, timedelta, timezone
from subreddits import subreddits
from helper.reddit import topPosts

DATABASE_URL = "postgresql://user:password@db:5432/praw_dashboard"

engine = sqlalchemy.create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

reddit = praw.Reddit("school")

def populate_authors(authors):
    for redditor in authors:
        if not redditor:
            continue
        author_name = redditor.name
        author = session.query(Author).filter_by(name=author_name).first()
        if not author:
            created = getattr(redditor, "created_utc", None)
            if created:
                created = datetime.fromtimestamp(created, tz=timezone.utc)
            author = Author(name=author_name, karma=getattr(redditor, "link_karma", 0) + getattr(redditor, "comment_karma", 0), created=created)
            session.add(author)
    session.commit()

def write_subreddit(subreddit_name):
    member = reddit.subreddit(subreddit_name).subscribers
    subreddit = session.query(Subreddit).filter_by(name=subreddit_name).first()
    if not subreddit:
        subreddit = Subreddit(name=subreddit_name)
        session.add(subreddit)
    member = Member(members_count = member, date=datetime.now(), subreddit = subreddit)
    session.add(member)

def populate_subreddits(subreddits):
    for subreddit_name in subreddits:
        write_subreddit(subreddit_name)
    session.commit()

def update():
    one_week_ago = datetime.now() - timedelta(days=7)
    recent_posts = session.query(Post).filter(Post.date >= one_week_ago).all()
    for post in recent_posts:
        submission = reddit.submission(post.submission_id)
        rating = SubmissionRating(
            post = post,
            num_comments=submission.num_comments,
            upvote_ratio=submission.upvote_ratio,
            score=submission.score,
            date = datetime.now()
        )
        session.add(rating)
    session.commit()
    

def populate_posts(df, subreddit_name):
    authors = df['author'].unique()
    populate_authors(authors)
    for _, row in df.iterrows():
        if not row['author']:
            continue
        author = session.query(Author).filter_by(name=row['author'].name).first()
        subreddit = session.query(Subreddit).filter_by(name=subreddit_name).first()
        post = session.query(Post).filter_by(submission_id=row['id']).first()
        if not post:
            post = Post(
                submission_id=row['id'],
                title=row['title'],
                date=row['date'],
                author_id=author.id,
                subreddit_id=subreddit.id,
                is_self=row['is_self'],
                is_original_content=row['is_original_content'],
                text=row['text'],
                flair=row['flair']
            )
            session.add(post)
        rating = SubmissionRating(
            post = post,
            num_comments=row['num_comments'],
            upvote_ratio=row['upvote_ratio'],
            score=row['score'],
            date = datetime.now()
        )
        session.add(rating)
    session.commit()

def gatherdata(df, subreddit):
    write_subreddit(subreddit)
    populate_posts(df, subreddit)
    print('collecting data for ', subreddit, 'at', datetime.now().strftime('%a %d %b %Y, %I:%M%p'))

def main():
    print("Database is set up")
    # populate_subreddits(subreddits)
    # for subreddit in subreddits:
    #     df = topPosts(subreddit, 10, 'day')
    #     populate_posts(df, subreddit)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    main()
