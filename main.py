import time

from model import *
from hashing import *

from google.appengine.api import users


class MainPage(BaseHandler):
    def get(self):

        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"

        products = get_products()

        # Check if there exists a product
        has_product = any(True for product in products if product)

        # Check if there exists a product on sale
        has_sale = any(True for product in products if product.sale)

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'categories': get_categories(),
            'products': products,
            'users': users,
            'has_sale': has_sale,
            'has_product': has_product
        }

        self.render('index.html', **template_values)


class AddProduct(BaseHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
            if not users.is_current_user_admin():
                self.redirect('/')

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"
            self.redirect('/')

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'categories': get_categories(),
            'products': get_products(),
            'users': users,
        }

        self.render('product_add.html', **template_values)

    def post(self):
        # find category and set key
        category_name = self.request.get('category')
        category = Categories.query(Categories.name == category_name).get()

        product = Product()
        product.category = category.key
        product.name = self.request.get('name')
        product.price = self.request.get('price')
        product.sale = self.request.get('sale')
        product.summary = self.request.get('summary')
        product.thumb = self.request.get('thumb')
        product.intro = self.request.get('intro')
        product.description = self.request.get('description')
        product.review = self.request.get('review')

        # get all URL -> list -> string
        list_image = self.request.get_all('pic_url')

        # remove empty element
        remove_empty(product.thumb, list_image)

        # a string represents a list that stores all images url
        product.image = str(list_image).strip('[]')

        if product.sale:
            product.sale_price = calculate_sale(product.price, product.sale)

        if len(product.summary) > 215:
            product.summary = product.summary[:product.summary.rfind(' ', 0, 220)] + '...'

        # store the data
        product.put()
        time.sleep(0.1)
        self.redirect('/product/' + str(product.key.id()))


class ProductPage(BaseHandler):
    def get(self, product_id):
        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"

        product = Product.get_by_id(int(product_id))

        images = product.image.replace("u'", '').replace("'", '').split(", ")

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'product': product,
            'categories': get_categories(),
            'products': get_products(),
            'users': users,
            'images': images
        }

        self.render('product.html', **template_values)


class EditProduct(BaseHandler):
    def get(self, product_id):
        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
            if not users.is_current_user_admin():
                self.redirect('/')

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"
            self.redirect('/')

        product = Product.get_by_id(int(product_id))

        images = product.image.replace("u'", '').replace("'", '').split(", ")
        images = images[1:]

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'product': product,
            'categories': get_categories(),
            'products': get_products(),
            'users': users,
            'product_key': product_id,
            'images': images
        }

        self.render('product_edit.html', **template_values)

    def post(self, product_id):

        # find category and set key
        category_name = self.request.get('category')
        category = Categories.query(Categories.name == category_name).get()

        product = Product.get_by_id(int(product_id))
        product.category = category.key
        product.name = self.request.get('name')
        product.price = self.request.get('price')
        product.sale = self.request.get('sale')
        product.summary = self.request.get('summary')
        product.thumb = self.request.get('thumb')
        product.intro = self.request.get('intro')
        product.description = self.request.get('description')
        product.review = self.request.get('review')

        # get all URL -> list -> string
        list_image = self.request.get_all('pic_url')

        # remove empty element
        remove_empty(product.thumb, list_image)

        # a string represents a list that stores all images url
        product.image = str(list_image).strip('[]')

        if product.sale:
            product.sale_price = calculate_sale(product.price, product.sale)

        if len(product.summary) > 215:
            product.summary = product.summary[:product.summary.rfind(' ', 0, 220)] + '...'

        # store the data
        product.put()
        time.sleep(0.1)
        self.redirect('/product/' + str(product.key.id()))


class DeleteProduct(webapp2.RequestHandler):
    def post(self, product_id):
        product = Product.get_by_id(int(product_id))
        product.key.delete()
        time.sleep(0.1)
        self.redirect('/admin')


class ManageCategory(BaseHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
            if not users.is_current_user_admin():
                self.redirect('/')

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"
            self.redirect('/')

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'categories': get_categories(),
            'products': get_products(),
            'users': users,
        }

        self.render('category_management.html', **template_values)

    def post(self):  # Add category
        name = self.request.get('category')

        # If not existed, change name
        if name and not exist_category(name):
            category = Categories()
            category.name = name
            category.put()

        time.sleep(0.1)
        self.redirect('/manage_category')


class EditCategory(BaseHandler):
    def post(self, category_id):
        name = self.request.get('category')
        category = Categories.get_by_id(int(category_id))

        # If not existed, change name
        if not exist_category(name):
            category.name = name
            category.put()

        time.sleep(0.1)
        self.redirect('/manage_category')


class Category(BaseHandler):
    def get(self, category_id):
        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"

        category = Categories.get_by_id(int(category_id))

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'category': category,
            'categories': get_categories(),
            'products': get_products(),
            'users': users,
        }

        self.render('category.html', **template_values)


class DeleteCategory(BaseHandler):
    def post(self, category_id):
        category = Categories.get_by_id(int(category_id))

        # Delete all products in the category then delete the category
        for product in get_products():
            if product.category == category.key:
                product.key.delete()

        category.key.delete()
        time.sleep(0.1)
        self.redirect('/manage_category')


class Contact(BaseHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'categories': get_categories(),
            'products': get_products(),
            'users': users,
        }

        self.render('contact.html', **template_values)


class AdminPage(BaseHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
            if not users.is_current_user_admin():
                self.redirect('/')
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"
            self.redirect('/')

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'categories': get_categories(),
            'products': get_products(),
            'users': users,
        }

        self.render('adminview.html', **template_values)


class About(BaseHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'categories': get_categories(),
            'products': get_products(),
            'users': users,
        }

        self.render('about.html', **template_values)


class Test(BaseHandler):
    def get(self):
        form_html = """
        <form>
        <h2>Add a Food</h2>
        <input type="text" name="food">
        <input type="hidden" name="food" value="egg">
        <button>Add</button>
        </form>
        """
        self.response.headers['Content-Type'] = 'text/plain'
        visits = 0
        visit_cookie_val = self.request.cookies.get('visits')
        if visit_cookie_val:
            cookie_val = check_secure_val(visit_cookie_val)
            if cookie_val:
                visits = int(cookie_val)

        visits += 1

        new_cookie_val = make_secure_val(str(visits))
        self.response.headers.add_header('Set-Cookie', 'visits=%s' % new_cookie_val)

        if visits > 10000:
            self.write("You are the best")
        else:
            self.write("You've been here %s times" % visits)


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/manage_category', ManageCategory),
    (r'/edit_category/(\w+)', EditCategory),
    (r'/category/(\w+)', Category),
    (r'/delete_category/(\w+)', DeleteCategory),
    ('/add_product', AddProduct),
    (r'/edit/(\w+)', EditProduct),
    (r'/delete_product/(\w+)', DeleteProduct),
    (r'/product/(\w+)', ProductPage),
    ('/admin', AdminPage),
    ('/contact', Contact),
    ('/about', About),
    ('/test', Test),

], debug=True)
