#!fl-mega/bin/python
import os
import unittest
from datetime import datetime, timedelta
from config import basedir
from moments import moments, db
from moments.models import User, Post

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


if __name__ == '__main__':
    unittest.main()
