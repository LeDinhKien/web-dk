import os

import time
from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape', 'jinja2.ext.loopcontrols'],
    autoescape=True)


class Categories(ndb.Model):
    name = ndb.StringProperty()


class Product(ndb.Model):
    category = ndb.KeyProperty(kind=Categories)
    name = ndb.StringProperty()
    price = ndb.StringProperty()
    summary = ndb.StringProperty(indexed=False)
    intro = ndb.StringProperty(indexed=False)
    description = ndb.StringProperty(indexed=False)
    image = ndb.StringProperty(indexed=False)
    review = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


# ===============================================MainPage===============================================================

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        addpage = ""
        addcategory = ""
        adminview = ""

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
            if users.is_current_user_admin():
                addpage = "Add Product"
                addcategory = "Manage Category"
                adminview = "Admin View"
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"

        category_query = Categories.query()
        categories = category_query.fetch()

        product_query = Product.query()
        products = product_query.fetch()

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'addpage': addpage,
            'addcategory': addcategory,
            'adminview': adminview,
            'categories': categories,
            'products': products,
            'users': users,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


# ===============================================AddPage================================================================

class AddProduct(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        addpage = ""
        addcategory = ""
        adminview = ""

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
            if users.is_current_user_admin():
                addpage = "Add Product"
                addcategory = "Manage Category"
                adminview = "Admin View"
            else:
                self.redirect('/')

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"
            self.redirect('/')

        # get category
        category_query = Categories.query()
        categories = category_query.fetch()

        # get product
        product_query = Product.query()
        products = product_query.fetch()

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'categories': categories,
            'products': products,
            'addpage': addpage,
            'addcategory': addcategory,
            'adminview': adminview,
            'users': users,
        }

        template = JINJA_ENVIRONMENT.get_template('product_add.html')
        self.response.write(template.render(template_values))

    def post(self):
        # find category and set key
        category_name = self.request.get('category')
        category = Categories.query(Categories.name == category_name).get()

        product = Product()
        product.category = category.key
        product.name = self.request.get('name')
        product.price = self.request.get('price')
        product.summary = self.request.get('summary')
        product.image = self.request.get('pic_url')
        product.intro = self.request.get('intro')
        product.description = self.request.get('description')
        product.review = self.request.get('review')

        # store the data
        product.put()
        self.redirect('/product/' + str(product.key.id()))


# ===============================================DetailPage=============================================================

class ProductPage(webapp2.RequestHandler):
    def get(self, id):
        user = users.get_current_user()

        addpage = ""
        addcategory = ""
        adminview = ""

        is_admin = users.is_current_user_admin()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
            if is_admin:
                addpage = "Add Product"
                addcategory = "Manage Category"
                adminview = "Admin View"

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"

        # get category
        category_query = Categories.query()
        categories = category_query.fetch()

        # get product
        product_query = Product.query()
        products = product_query.fetch()

        product = Product.get_by_id(int(id))

        images = [product.image,
                  'https://lh3.googleusercontent.com/TOATo5DampvMiBzCBRqIskWIt3tN65n1BAA5yT3zlU-W63zKgwQotF998IAHiXpiWlZDtTUkrw',
                  '/images/rivalfade.png',
                  '/images/STEELSERIES_SIBERIA.png',
                  '/images/pulse.jpg',
                  '/images/K70RGB.png',
                  'http://www.alina.se/images/produktbilder/thumb/800/tn_c84e85dc73324397cd9d7d547c4d6570.png']

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'addpage': addpage,
            'addcategory': addcategory,
            'adminview': adminview,
            'is_admin': is_admin,
            'product': product,
            'products': products,
            'categories': categories,
            'users': users,
            'images': images
        }
        template = JINJA_ENVIRONMENT.get_template('product.html')
        self.response.write(template.render(template_values))


# ===============================================EditPage===============================================================

class EditProduct(webapp2.RequestHandler):
    def get(self, id):
        user = users.get_current_user()

        addpage = ""
        addcategory = ""
        adminview = ""

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
            if users.is_current_user_admin():
                addpage = "Add Product"
                addcategory = "Manage Category"
                adminview = "Admin View"
            else:
                self.redirect('/')

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"
            self.redirect('/')

        # get category
        category_query = Categories.query()
        categories = category_query.fetch()

        # get product
        product_query = Product.query()
        products = product_query.fetch()

        product = Product.get_by_id(int(id))

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'addpage': addpage,
            'addcategory': addcategory,
            'adminview': adminview,
            'categories': categories,
            'product': product,
            'products': products,
            'users': users,
        }

        template = JINJA_ENVIRONMENT.get_template('product_edit.html')
        self.response.write(template.render(template_values))

    def post(self, id):

        # find category and set key
        category_name = self.request.get('category')
        category = Categories.query(Categories.name == category_name).get()

        product = Product.get_by_id(int(id))
        product.category = category.key
        product.name = self.request.get('name')
        product.price = self.request.get('price')
        product.summary = self.request.get('summary')
        product.image = self.request.get('pic_url')
        product.intro = self.request.get('intro')
        product.description = self.request.get('description')
        product.review = self.request.get('review')

        # store the data
        product.put()
        time.sleep(0.1)
        self.redirect('/product/' + str(product.key.id()))


# ===============================================DeleteProduct==========================================================

class DeleteProduct(webapp2.RequestHandler):
    def post(self, id):
        product = Product.get_by_id(int(id))
        product.key.delete()
        time.sleep(0.1)
        self.redirect('/admin')


# ===============================================ManageCategory=========================================================

class ManageCategory(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        addpage = ""
        addcategory = ""
        adminview = ""

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
            if users.is_current_user_admin():
                addpage = "Add Product"
                addcategory = "Manage Category"
                adminview = "Admin View"
            else:
                self.redirect('/')

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"
            self.redirect('/')

        category_query = Categories.query()
        categories = category_query.fetch()

        product_query = Product.query()
        products = product_query.fetch()

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'addpage': addpage,
            'addcategory': addcategory,
            'adminview': adminview,
            'categories': categories,
            'products': products,
            'users': users,
        }

        template = JINJA_ENVIRONMENT.get_template('category_management.html')
        self.response.write(template.render(template_values))

    def post(self):  # Add category
        name = self.request.get('category')

        category_query = Categories.query()
        categories = category_query.fetch()

        not_stored = True
        for category in categories:
            if category.name.lower() == name.lower():
                not_stored = False

        if not_stored:
            category = Categories()
            category.name = name
            category.put()

        time.sleep(0.1)
        self.redirect('/manage_category')


# ===============================================EditCategory===========================================================

class EditCategory(webapp2.RequestHandler):
    def post(self, id):
        name = self.request.get('category')
        category = Categories.get_by_id(int(id))

        category_query = Categories.query()
        categories = category_query.fetch()

        # Check if name existed
        not_stored = True
        for cat in categories:
            if cat.name.lower() == name.lower():
                not_stored = False

        # If not existed, change name
        if not_stored:
            category.name = name
            category.put()

        time.sleep(0.1)
        self.redirect('/manage_category')


# ===============================================CategoryDetail=========================================================

class Category(webapp2.RequestHandler):
    def get(self, id):
        user = users.get_current_user()

        addpage = ""
        addcategory = ""
        adminview = ""

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
            if users.is_current_user_admin():
                addpage = "Add Product"
                addcategory = "Manage Category"
                adminview = "Admin View"
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"

        category = Categories.get_by_id(int(id))

        category_query = Categories.query()
        categories = category_query.fetch()

        # get product
        product_query = Product.query()
        products = product_query.fetch()

        for prod in products:
            if len(prod.summary) > 219:
                prod.summary = prod.summary[:prod.summary.rfind(' ', 0, 220)] + '...'

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'category': category,
            'addpage': addpage,
            'addcategory': addcategory,
            'adminview': adminview,
            'products': products,
            'categories': categories,
            'users': users,
        }

        template = JINJA_ENVIRONMENT.get_template('category.html')
        self.response.write(template.render(template_values))


# =============================================DeleteCategory===========================================================

class DeleteCategory(webapp2.RequestHandler):
    def post(self, id):
        category = Categories.get_by_id(int(id))
        product_query = Product.query()
        products = product_query.fetch()

        # Delete all products in the category then delete the category
        for product in products:
            if product.category == category.key:
                product.key.delete()

        category.key.delete()
        time.sleep(0.1)
        self.redirect('/manage_category')


# ============================================Contact Page==============================================================

class Contact(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        addpage = ""
        addcategory = ""
        adminview = ""

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
            if users.is_current_user_admin():
                addpage = "Add Product"
                addcategory = "Manage Category"
                adminview = "Admin View"
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"

        category_query = Categories.query()
        categories = category_query.fetch()

        product_query = Product.query()
        products = product_query.fetch()

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'addpage': addpage,
            'addcategory': addcategory,
            'adminview': adminview,
            'categories': categories,
            'products': products,
            'users': users,
        }

        template = JINJA_ENVIRONMENT.get_template('contact.html')
        self.response.write(template.render(template_values))


# ===============================================AdminView==============================================================

class AdminPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        addpage = ""
        addcategory = ""
        adminview = ""

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
            if users.is_current_user_admin():
                addpage = "Add Product"
                addcategory = "Manage Category"
                adminview = "Admin View"
            else:
                self.redirect('/')

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"
            self.redirect('/')

        category_query = Categories.query()
        categories = category_query.fetch()

        product_query = Product.query()
        products = product_query.fetch()

        for prod in products:
            if len(prod.summary) > 219:
                prod.summary = prod.summary[:prod.summary.rfind(' ', 0, 220)] + '...'

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'addpage': addpage,
            'addcategory': addcategory,
            'adminview': adminview,
            'products': products,
            'categories': categories,
            'users': users,
        }

        template = JINJA_ENVIRONMENT.get_template('adminview.html')
        self.response.write(template.render(template_values))


# ============================================About Page==============================================================

class About(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        addpage = ""
        addcategory = ""
        adminview = ""

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
            if users.is_current_user_admin():
                addpage = "Add Product"
                addcategory = "Manage Category"
                adminview = "Admin View"
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"

        category_query = Categories.query()
        categories = category_query.fetch()

        product_query = Product.query()
        products = product_query.fetch()

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'addpage': addpage,
            'addcategory': addcategory,
            'adminview': adminview,
            'categories': categories,
            'products': products,
            'users': users,
        }

        template = JINJA_ENVIRONMENT.get_template('about.html')
        self.response.write(template.render(template_values))


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
    ('/about', About)
], debug=True)
