from helper.reddit import topPosts
from subreddits import subreddits
from populate_db import gatherdata
from datetime import datetime 

def main():
    print('hourly script called', datetime.now().strftime('%a %d %b %Y, %I:%M%p'))
    for subreddit in subreddits:
        df =topPosts(time_filter='day', limit=10, subreddit_name=subreddit)
        gatherdata(df, subreddit)

if __name__ == "__main__":
    main()
