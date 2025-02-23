import praw, pandas as pd, os.path, re

reddit = praw.Reddit("school")

"""
fragt die Reddit Api ab und füllt ein dataframe mit verschiedenen Daten aus Reddit
"""

def topPosts(subreddit_name: str, limit = 1000, time_filter='all'):
    """
    time_filter – Can be one of: "all", "day", "hour", "month", "week", or "year" (default: "all").
    """
    subreddit = reddit.subreddit(subreddit_name)
    top_posts = subreddit.top(limit=limit, time_filter=time_filter)

    # declarations
    titles = []
    scores = []
    dates = []
    ids = []
    upvote_ratios = []
    authors = []
    num_comments = []
    is_self = []
    is_original_content = []
    texts = []
    flair = []

    # gathering data
    for post in top_posts:
        titles.append(post.title)
        scores.append(post.score)
        dates.append(pd.to_datetime(post.created_utc, utc=True, unit='s'))
        ids.append(post.id)
        upvote_ratios.append(post.upvote_ratio)
        authors.append(post.author)
        num_comments.append(post.num_comments)
        is_self.append(post.is_self)
        is_original_content.append(post.is_original_content)
        texts.append(post.selftext)
        flair.append(post.link_flair_text)

    df = pd.DataFrame({
        'id': ids,
        'title': titles,
        'score': scores,
        'date': dates,
        'upvote_ratio': upvote_ratios,
        'author': authors,
        'num_comments': num_comments,
        'is_self': is_self,
        'is_original_content': is_original_content,
        'text': texts,
        'flair': flair
    })
    return df

def word_n_gram(text: str, n = 2, counter = {}):
    search_window = []
    cleaned_string = re.sub(r'[^a-zA-Z0-9äöüß_\-% ]', '', text.lower())
    for word in cleaned_string.split():
        search_window.append(word)
        if len(search_window) == n:
            key = tuple(search_window)
            if key in counter:
                counter[key] +=1
            else:
                counter[key] = 1
            search_window.pop(0)

    return counter

def get_n_gram_series(subreddit_name, n=2, use_file=True):
    filename = f'text/{subreddit_name}/{n}-gram.csv'
    if(use_file and os.path.isfile(filename)):
        #reads file and uses all the columns except the last one as index and return a Series
        return pd.read_csv(filename, index_col=list(range(len(pd.read_csv(filename, nrows=0).columns) - 1))).iloc[:, -1]
    counter = {}
    os.makedirs(f'text/{subreddit_name}', exist_ok=True)
    df = topPosts(subreddit_name)
    for _, post in df.iterrows():
        counter = word_n_gram(n=n, text=post['title'], counter=counter)
        if(post['is_self']):
            counter = word_n_gram(n=n, text=str(post['text']), counter=counter)
    ngs = pd.Series(counter)
    ngs = ngs.sort_values(ascending=False)
    ngs.to_csv(filename)
    return ngs



