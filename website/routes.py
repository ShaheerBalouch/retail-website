from flask import Flask, render_template, url_for, request, redirect, flash
from website.models import User, Shopping_Cart, Items, Wishlist
from website import app, db
from website.forms import RegistrationForm, LoginForm, CheckoutForm
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/")
@app.route("/home/<sorter>")
def home(sorter='id'):
    items=Items.query.all()
    
    return render_template('home.html', items=items, sorter=sorter)


@app.route("/messages")
def messages():
    return render_template('messages.html', title='message')



@app.route("/about")
def about():
    return render_template('about.html', title='About Us')



@app.route("/item/<int:item_id>")
def item(item_id):
    items = Items.query.get_or_404(item_id)
    return render_template('item.html', title=items.name, items=items)
    



@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        
        user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Thank You For Registering '+user.username+'!')
        return redirect(url_for('messages'))
    
    return render_template('register.html', title='Register', form=form)



@app.route("/cart")
@login_required
def cart():

    cartItems = Shopping_Cart.query.filter(Shopping_Cart.user_id == current_user.id)

    return render_template('cart.html', title='Your Shopping Cart', cartItems=cartItems, user=current_user.id)

@app.route("/wishlist")
@login_required
def wishlist():
    
    wishItems = Wishlist.query.filter(Wishlist.user_id == current_user.id)

    return render_template('wishlist.html', title='Your Wishlist', wishItems=wishItems, user=current_user.id)


@app.route("/add_item/<int:item_id>")
def add_item(item_id):

    if not(current_user.is_authenticated):
        flash('You need to be logged in to add an item to the Cart!')
        return redirect(url_for('login'))
        
    
    item=Items.query.get_or_404(item_id)
    cartItems = Shopping_Cart.query.filter(Shopping_Cart.user_id==current_user.id)
    Wishlist.query.filter(Wishlist.item_id==item_id and Wishlist.user_id==current_user.id).delete()

    
    if cartItems is not None:
        
        for thing in cartItems:
            
            if item_id == thing.item_id:

                thing.quantity+=1
                db.session.commit()
                flash("Item successfully added to the Cart!")
                return redirect(url_for('messages'))
        


    db.session.add(Shopping_Cart(item_id=item.id, user_id=current_user.id, quantity=1))

    db.session.commit()
    flash("Item successfully added to the Cart!")
    return redirect(url_for('messages'))
    

@app.route("/add_wish/<int:item_id>")
def add_wish(item_id):
    
    if not(current_user.is_authenticated):
        flash('You need to be logged in to save an item to the Wishlist!')
        return redirect(url_for('login'))
    
    item=Items.query.get_or_404(item_id)
    wishItems = Wishlist.query.filter(Wishlist.user_id==current_user.id)

    if wishItems is not None:
        for thing in wishItems:

            if item_id == thing.item_id:

                thing.quantity+=1
                db.session.commit()
                flash("Item successfully added to the Wishlist!")
                return redirect(url_for('messages'))
            

        
    db.session.add(Wishlist(item_id=item.id, user_id=current_user.id, quantity=1))

    db.session.commit()
    flash("Item successfully added to wishlist!")
    return redirect(url_for('messages'))



@app.route("/remove_wish/<int:item_id>")
@login_required
def remove_wish(item_id):
    Wishlist.query.filter(Wishlist.item_id==item_id and Wishlist.user_id==current_user.id).delete()
    
    
    db.session.commit()
    return redirect(url_for('wishlist'))

    

@app.route("/remove_item/<int:item_id>")
@login_required
def remove_item(item_id):
    Shopping_Cart.query.filter(Shopping_Cart.item_id==item_id and Shopping_Cart.user_id==current_user.id).delete()
    
    
    db.session.commit()
    return redirect(url_for('cart'))


@app.route("/one_item/<int:item_id>")
@login_required
def one_item(item_id):
    item = Shopping_Cart.query.filter(Shopping_Cart.item_id==item_id and Shopping_Cart.user_id==current_user.id)

    for thing in item:
        
        if thing.quantity>=2:
            thing.quantity-=1
            
        else:
            item.delete()

    db.session.commit()
    return redirect(url_for('cart'))


@app.route("/one_wish/<int:item_id>")
def one_wish(item_id):
    item = Wishlist.query.filter(Wishlist.item_id==item_id and Wishlist.user_id==current_user.id)

    for thing in item:
        
        if thing.quantity>=2:
            thing.quantity-=1
            
        else:
            item.delete()

    db.session.commit()
    return redirect(url_for('wishlist'))
    

    

@app.route("/checkout", methods=['GET', 'POST'])
@login_required
def checkout():
    form=CheckoutForm()
    if form.validate_on_submit():
        
        Shopping_Cart.query.filter(Shopping_Cart.user_id==current_user.id).delete()
        
        
        db.session.commit()

        flash('Payment Received!')
        return redirect(url_for('messages'))
    
    return render_template('checkout.html', title='Checkout', form=form)
        


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('Login Successful! Welcome '+user.username)
            return redirect(url_for('messages'))
        
        else:
            flash('Invalid email or password')
        
        
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logout Successful!')
    return redirect(url_for('messages'))


