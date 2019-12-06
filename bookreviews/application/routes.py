from flask import render_template, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from application import app, db, bcrypt, login_manager
from application.models import Reviews, Users
from application.forms import ReviewsForm, LoginForm, RegisterForm, UpdateAccountForm, EditForm


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))

    return render_template('login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        user = Users(email=form.email.data, 
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/reviews')
def reviews():
    postData = Reviews.query.all()
    return render_template('reviews.html', title='Reviews', reviews = postData)

@app.route('/post', methods=['GET','POST'])
@login_required
def post():
    form = ReviewsForm()
    if form.validate_on_submit():
        postData = Reviews(
        title=form.title.data,
        author=form.author.data,
        rating=form.rating.data,
        review=form.review.data,
        user=current_user
    )

        db.session.add(postData)
        db.session.commit()
        return redirect(url_for('home'))

    else:
        print(form.errors)
    return render_template('post.html', title='Post', form=form)

login_manager.init_app(app)
@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.delete.data:
            user_id = Users.query.filter_by(id=current_user.id).first()
            db.session.delete(user_id)
            review_id = Reviews.query.filter_by(user_id=None)
            for deleted in review_id:
                db.session.delete(deleted)
            db.session.commit()
            return redirect (url_for('login'))
        elif form.submit.data:
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.email = form.email.data
            db.session.commit()
            return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    postData = Reviews.query.filter_by(user_id=current_user.id).all()
    return render_template('account.html', title='Account', form=form, account=postData)

@app.route('/edit/<int:review_id>', methods =['GET', 'POST'])
@login_required
def edit(review_id):   
    review = Reviews.query.filter_by(id=review_id).first()
    user_reviews=Reviews.query.filter_by(user_id=current_user.id)
    list=[]
    for all in user_reviews:
        allid = all.id
        list.append(allid)
    if review_id in list:
        form = EditForm()
        if request.method == 'GET':
            form.title.data = review.title
            form.author.data = review.author
            form.rating.data = review.rating
            form.review.data = review.review
        elif form.validate_on_submit():
            if form.delete.data:
                db.session.delete(review)
                db.session.commit()
                return redirect (url_for('reviews'))
            elif form.submit.data:
                review.title = form.title.data
                review.author = form.author.data
                review.rating = form.rating.data
                review.review = form.review.data
                db.session.commit()
                return redirect (url_for('home'))
        #if request.method == 'GET':
           # form.title.data = review.title
           # form.author.data = review.author
           # form.rating.data = review.rating
           # form.review.data = review.review
    else:
        return redirect (url_for ('home'))
    return render_template('edit.html', title='Edit', form=form)



