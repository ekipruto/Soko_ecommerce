from flask import Blueprint, render_template, flash, send_from_directory, redirect
from flask_login import login_required, current_user
from .forms import ShopItemsForm,OrderForm
from werkzeug.utils import secure_filename
from .models import Product, Order,Customer
from . import db

admin=Blueprint('admin', __name__)

#this is for viewing the product images fetched from the db
@admin.route('/media/<path:filename>')   
def get_image(filename):
    return send_from_directory('../media', filename)

#updating the items
@admin.route('/update-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    if current_user.id==1:
        form=ShopItemsForm()
        item_to_update=Product.query.get(item_id)

        #fetching items from db
        form.product_name.render_kw = {'placeholder': item_to_update.product_name}
        form.previous_price.render_kw = {'placeholder': item_to_update.previous_price}
        form.current_price.render_kw = {'placeholder': item_to_update.current_price}
        form.in_stock.render_kw = {'placeholder': item_to_update.in_stock}
        form.flash_sale.render_kw = {'placeholder': item_to_update.flash_sale}

        #validating user inputs
        if form.validate_on_submit():

            product_name=form.product_name.data
            current_price=form.current_price.data
            previous_price=form.previous_price.data
            in_stock=form.in_stock.data
            flash_sale=form.flash_sale.data

            file = form.product_picture.data

            file_name = secure_filename(file.filename)
            file_path = f'./media/{file_name}'

            file.save(file_path)
             
            #commiting changes to the db
            try:
                Product.query.filter_by(id=item_id).update(dict(product_name=product_name,
                                                                current_price=current_price,
                                                                previous_price=previous_price,
                                                                in_stock=in_stock,
                                                                flash_sale=flash_sale,
                                                                product_picture=file_path))

                db.session.commit()
                flash(f'{product_name} updated Successfully')
                print('Product Upadted')
                return redirect('/shop-items')
            except Exception as e:
                print('Product not Upated', e)
                flash('Item Not Updated!!!')

        return render_template('update-item.html', form=form)
    return render_template('404.html')

#deleting  item(s)
@admin.route('/delete-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    if current_user.id==1:
        try:
            item_to_delete=Product.query.get(item_id)
            db.session.delete(item_to_delete)
            db.session.commit()
            flash('One Item has been deleted')
            return redirect('/shop-items')
        
        except Exception as e:
            print('Item not deleted', e)
            flash(f'Item not deleted')
            return redirect('/shop-items')
    return render_template('404.html')


#Adding the products to the db
@admin.route('/add-shop-items', methods=['POST','GET'])
@login_required
def add_shop_items():
    if current_user.id==1:
        form=ShopItemsForm()
        if form.validate_on_submit():
            product_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data
            in_stock = form.in_stock.data
            flash_sale = form.flash_sale.data

            file=form.product_picture.data
            file_name=secure_filename(file.filename) #this removes whitespaces and invallid characters from filename

            file_path = f'./media/{file_name}'

            file.save(file_path)

            new_shop_item=Product()
            new_shop_item.product_name=product_name
            new_shop_item.current_price=current_price
            new_shop_item.previous_price=previous_price
            new_shop_item.in_stock=in_stock
            new_shop_item.flash_sale=flash_sale

            new_shop_item.product_picture=file_path

            try:
                db.session.add(new_shop_item)
                db.session.commit()
                flash(f'{product_name}, Added Successfully')

                return render_template('add-shop-items.html', form=form)

            except Exception as e:
                print(e)
                flash('Product item not added')

        return render_template('/add-shop-items.html', form=form)
    return render_template('404.html')

#Displaying the item list
@admin.route('/shop-items', methods=['POST','GET'])
@login_required
def shop_items():
    if current_user.id==1:
        items=Product.query.order_by(Product.date_added).all()   #items is the list of all the items in the shop
        return render_template('shop-items',items=items)
    return render_template('404.html')

@admin.route('/view-orders')
@login_required
def view_orders():
    if current_user.id == 1:
        orders = Order.query.all()
        return render_template('view_orders.html', orders=orders)
    return render_template('404.html')

@admin.route('/order_update/<int:order_id>', methods=['GET', 'POST'])
@login_required
def order_update(order_id):
    if current_user.id==1:
        form=OrderForm
        order=Order.query.get(order_id)

        if form.validate_on_submit():
            status=form.order_status.data
            order.status=status

            try:
                db.session.commit()
                flash(f'order {order_id} updated successfully')
                return redirect('view-orders')
            except Exception as e:
                print(e)
                flash(f'order {order_id} not updated')
                return redirect('view-orders')

        return render_template('order_update.html', form=form)
    return render_template('404.html')

@admin.route('/customers')
@login_required
def display_customers():
    if current_user.id == 1:
        customers = Customer.query.all()
        return render_template('customers.html', customers=customers)
    return render_template('404.html')

@admin.route('/admin')
@login_required
def admin_page():
    if current_user.id==1:
        return render_template ('admin.html')
    return render_template('404.html')

