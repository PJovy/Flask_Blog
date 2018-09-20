import json
from flaskblog import db
from flaskblog.models import Post
import time
import math


def import_posts():
    with open('posts.json', 'r') as f:
        posts = json.load(f)
        for p in posts:
            post = Post(title=p['title'], content=p['content'], user_id=p['user_id'])
            db.session.add(post)
            db.session.commit()
            time.sleep(1)

def delete_posts():
    Post.query.delete()
    db.session.commit()


def query_total_pagenum(per_page):
    p_m = math.ceil(Post.query.paginate().total/per_page)
    return p_m



if __name__ == '__main__':
    # query_total_pagenum()
    print(query_total_pagenum(5))
    # import_posts()
    # delete_posts()
