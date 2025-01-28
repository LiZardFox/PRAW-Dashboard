from reddit import fetch_posts_daily
if __name__ == "__main__":
    subreddits = ['ask', 'politics', 'Python', 'ProgrammerHumor', 'ich_iel']
    for subreddit in subreddits:
        fetch_posts_daily(subreddit)