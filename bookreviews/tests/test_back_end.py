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
        review = Reviews(title="example", author="anon", rating="5", review="Mediocre", user_id="2")

        #save review to database
        db.session.add(review)
        db.session.commit

        self.assertEqual(Reviews.query.count(), 1)

        #update information
        review.author = "Anonymous"
        db.session.commit

        self.assertEqual(Reviews.query.filter_by(title='example').first().author, "Anonymous")

        #delete record
        db.session.delete(review)
        db.session.commit

        self.assertEqual(Reviews.query.count(), 0)

    def test_user(self):
        """
        Test number of users in user table and user information after creating, updating and deleting a record
        """

        # create test review
        user = Users(first_name="Nick", last_name="Jones", email="nickjones@yahoo.com", password="password")
    

        #save review to database
        db.session.add(user)
        db.session.commit

        self.assertEqual(Users.query.count(), 3)

        #update information
        user.first_name = "Nicholas"
        db.session.commit

        self.assertEqual(Users.query.filter_by(email='nickjones@yahoo.com').first().first_name, "Nicholas")
        
        #delete record
        db.session.delete(user)
        db.session.commit

        self.assertEqual(Users.query.count(), 2)

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

    def test_post_view(self):
        """
        Test that the post page is inaccessiable without login and redirects to the login page and then to the dashboard
        """
        target_url = url_for('post', user_id=2)
        redirect_url = url_for('login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


    def test_home_view(self):
        """
        Test that the home page is accessible without login
        """
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code, 200)

    def test_about_view(self):
        """
        Test that the about page is accessible without login
        """
        response = self.client.get(url_for('about'))
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        """
        Test that the register page is accessible without login
        """
        response = self.client.get(url_for('register'))
        self.assertEqual(response.status_code, 200)

    def test_reviews_view(self):
        """
        Test that the login page is accessible without login
        """
        response = self.client.get(url_for('reviews'))
        self.assertEqual(response.status_code, 200)




    
