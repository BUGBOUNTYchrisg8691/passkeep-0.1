#!/usr/bin/env python3

from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authentication = db.Column(db.Boolean, default=False)

    def is_active(self):
        return True

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)
@bull.route('/reports')
@login_required
def reports():
    products = Product.query.all()
    purchases = Purchase.query.all()
    purchases_by_day = dict()
    for purchase in purchases:
        purchase_date = purchase.sold_at.date().strftime('%m-%d')
        if purchase_date not in purchases_by_day:
            purchases_by_day[purchase_date] = {'units': 0, 'sales': 0.00}
        purchases_by_day[purchase_date]['units'] += 1
        purchases_by_day[purchase_date]['sales'] += purchase.product.price
    purchase_day = sorted(purchases_by_day.keys())
    units = len(purchases)
    total_sales = sum([p.product.price for p in purchases])

    return render_template(
        'reports.html',
        products=products,
        purchase_days=purchase_days,
        purchases=purchases,
        purchases_by_day=purchases_by_day,
        units=units,
        total_sales=total_sales
    )

@bull.route('/login', methods=['GET', 'POST'])
def login():
    print db
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.email.data)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect(url_for('bull.reports'))
    return render_template('login.html', form=form)

@bull.route('/logout', methods=['GET'])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template('logout.html')
