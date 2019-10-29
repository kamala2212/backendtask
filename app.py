# import the Flask class from the flask module
from flask import Flask, render_template, request, redirect, session
from models import *

# create the application object
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route('/register', methods=['GET', 'POST'])
def register():
	form = SignupForm()
	if request.method == 'GET':
		return render_template('register.html', form=form)
		
	elif request.method == 'POST':
		
		if form.validate():
			if User.query.filter_by(email=form.email.data).first():
				flash("Email already exists, please use another email.", 'warning')
				#return render_template('register.html', form = form)
			else:
				newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
				db.session.add(newuser)
				db.session.commit()

				session['email'] = newuser.email
				session["user_id"] = newuser.id
				flash("Account created, you are now logged in.", 'success')
		else:
			# error has occured
			for field, errors in form.errors.items():
				for error in errors:
					flash(u"Error in the %s field - %s" % (getattr(form, field).label.text,error), "warning")
#return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'email' in session:
		flash("You are already signed in.", 'success')
	
	form = SigninForm()
	if request.method == 'POST':
		email = form.email.data
		password = form.password.data
		user = User.query.filter_by(email=email).first()

		if user is not None and user.check_password(password):
			session['email'] = email
			session['user_id'] = user.id
			flash("Logged in successfully.", 'success')

		else: 
			flash("Incorrect username or password. Please try again.", 'success')	
			
	elif request.method == 'GET':
		return render_template("login.html", form=form)

@app.route('/lost')
def lost():
	title = 'Lost'
	item_post = models.Items(item_status='lost')
	#return render_template("lost.html",item_posts = item_post,title = title)

@app.route('/found')
def found():
	title = 'Found'
	item_post = models.Items.query.filter_by(item_status='found')
	#return render_template("lost.html",item_posts = item_post,title = title)							


@app.route('/item')
def item():
	item_param = request.args.get('id','item_id')
	title = 'Item #' + item_param
	item_post = models.Items.query.filter_by(id=item_param) 
	#return render_template("items.html",item_posts =item_post,title = title)

@app.route('/add', methods = ['GET', 'POST'])
def add():
	title = "Post Item"
	form = PostItem()
	if form.validate_on_submit():
		post = Items(name_item = form.item_name.data,description=form.descrip.data, 
					date=datetime.datetime.utcnow(), item_status=form.item_status.data,
					area=form.location.data)
		db.session.add(post)
		db.session.commit()

	#return render_template("add.html",title = title,form = form)


# start the server with the 'run()' method
if __name__ == '__main__':
	app.run(debug=True)
