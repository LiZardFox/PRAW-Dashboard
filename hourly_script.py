from helper.reddit import topPosts
from subreddits import subreddits
from populate_db import gatherdata

def main():
    for subreddit in subreddits:
        df =topPosts(time_filter='day', limit=10, subreddit_name=subreddit)
        gatherdata(df, subreddit)

if __name__ == "__main__":
    main()
