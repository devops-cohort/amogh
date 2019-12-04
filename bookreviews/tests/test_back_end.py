import unittest

from flask import abort, url_for
from flask_testing import TestCase
from os import getenv
from application import app, db
from application.models import Users, Reviews

class TestBase(TestCase):

    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql+pymysql://'+str(getenv('MYSQL_USER'))+':'+str(getenv('MYSQL_PASSWORD'))+'@'+str(getenv('MYSQL_IP'))+'/'+str(getenv('MYSQL_DB_TEST')),
            SQLALCHEMY_SECRET_KEY = str(getenv('MYSQL_KEY')))

        return app

    def setUp(self):
        """
        Will be called before every test
        """

        db.session.commit()
        db.drop_all()
        db.create_all()

        # create test admin user
        admin = Users(first_name="admin", last_name="admin", email="admin@admin.com", password="admin2016")

        # create test non-admin user
        employee = Users(first_name="test", last_name="user", email="test@user.com", password="test2016")

        # save users to database
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()

class TestFeatures(TestBase):

    def test_review(self):
        """
        Test number of reviews in review table
        """

        # create test review
        user = Users(first_name="Bob", last_name="Jones", email="bobjones@yahoo.com", password="password")
        review = Reviews(title="example", author="anon", rating="5", review="Mediocre", user_id="1")

        #save review to database
        db.session.add(review)
        db.session.commit

        self.assertEqual(Reviews.query.count(), 1)

    def test_login_view(self):
        """
        Test that the login page is accessible without login
        """
        response = self.client.get(url_for('login'))
        self.assertEqual(response.status_code, 200)

    def test_account_view(self):
        """
        Test that the account page is inaccessiable without login and redirects to the login page and then to the dashboard
        """
        target_url = url_for('account', user_id=2)
        redirect_url = url_for('login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


    
