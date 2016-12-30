#!fl-mega/bin/python
import os
import unittest
from datetime import datetime, timedelta
from config import basedir
from moments import moments, db
from moments.models import User, Post, Tag, postTags
from datetime import datetime, timedelta

# a more complex setup could include several groups of tests each represented
# by a untittest.TestCase subclass, and each group then would have
# independent setUp an tearDown methods

class TestCase(unittest.TestCase):
    # run before each test
    def setUp(self):
        moments.config['TESTING'] = True
        moments.config['WTF_CSRF_ENABLED'] = False
        moments.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.moments = moments.test_client()
        db.create_all()

    # run after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_account(self):
        """
        Verifies if a account is really created
        """
        u = User(username='me', email='me@gmail.com', password='123456', firstname='moa')
        db.session.add(u)
        db.session.commit()
        userlist = User.query.all()
        for user in userlist:
            print user.username
            print user.email
            print user.firstname
            print user.password

    def test_tags_posts(self):
        """
        Tests the tags and posts relationship
        """
        u1 = User(username='me', email='me@gmail.com', password='123456', firstname='moa')
        db.session.add(u1)
        db.session.commit()
        u = User.query.filter_by(username=u1.username).first()
        print u
        utcnow = datetime.utcnow()
        post = Post(body="testing post", user_id=u.id, timestamp=utcnow+timedelta(seconds=1))
        woo = Tag(tag="woo")
        post2 = Post(body="testing post 2", user_id=u.id, timestamp=utcnow+timedelta(seconds=4))

        woo.posts.append(post)
        woo.posts.append(post2)
        db.session.add(post)
        db.session.add(woo)
        db.session.add(post2)
        db.session.commit()
        wood = Tag.query.filter_by(tag="woo").first()
        print wood
        print wood.tag
        print wood.posts
        for wp in wood.posts:
            print wp
        #wlist = wood.posts.filter_by(postTags.c.tag == wood.tag).all()
        #wlist = Tag.query.filter_by(tag="woo").all()
        wlist = Post.query.join(postTags).filter(postTags.c.tag == wood.tag).order_by(Post.timestamp.desc()).all()
        print wlist

if __name__ == '__main__':
    unittest.main()
