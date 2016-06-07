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
    intro = ndb.StringProperty(indexed=False)
    description = ndb.StringProperty(indexed=False)
    image = ndb.StringProperty()
    review = ndb.StringProperty()


# ===============================================MainPage================================================================

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
                addpage = "Add Page"
                addcategory = "Add Category"
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


# ===============================================AddPage=================================================================

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
                addpage = "Add Page"
                addcategory = "Add Category"
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

        template = JINJA_ENVIRONMENT.get_template('addpage.html')
        self.response.write(template.render(template_values))

    def post(self):
        # find category and set key
        category_name = self.request.get('category')
        category = Categories.query(Categories.name == category_name).get()

        product = Product()
        product.category = category.key
        product.name = self.request.get('name')
        product.image = self.request.get('pic_url')
        product.intro = self.request.get('intro')
        product.description = self.request.get('description')
        product.review = self.request.get('review')

        # store the data
        product.put()
        self.redirect('/product/' + str(product.key.id()))


# ===============================================AdminView=============================================================

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
                addpage = "Add Page"
                addcategory = "Add Category"
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
            'products': products,
            'categories': categories,
            'users': users,
        }

        template = JINJA_ENVIRONMENT.get_template('adminview.html')
        self.response.write(template.render(template_values))

    def post(self):
        category_name = self.request.get('category')
        category = Categories.query(Categories.name == category_name).get()


# ===============================================DetailPage==============================================================

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
            if users.is_current_user_admin():
                addpage = "Add Page"
                addcategory = "Add Category"
                adminview = "Admin View"

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"

        category_query = Categories.query()
        categories = category_query.fetch()

        product = Product.get_by_id(int(id))

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'addpage': addpage,
            'addcategory': addcategory,
            'adminview': adminview,
            'is_admin': is_admin,
            'product': product,
            'categories': categories,
            'users': users,
        }
        template = JINJA_ENVIRONMENT.get_template('detail.html')
        self.response.write(template.render(template_values))

    def post(self, id):
        product = Product.get_by_id(int(id))
        self.redirect('/adminview')


# ===============================================EditPage================================================================

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
                addpage = "Add Page"
                addcategory = "Add Category"
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

        product = Product.get_by_id(int(id))

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'addpage': addpage,
            'addcategory': addcategory,
            'adminview': adminview,
            'categories': categories,
            'product': product,
            'users': users,
        }

        template = JINJA_ENVIRONMENT.get_template('editpage.html')
        self.response.write(template.render(template_values))

    def post(self, id):

        # find category and set key
        category_name = self.request.get('category')
        category = Categories.query(Categories.name == category_name).get()

        product = Product.get_by_id(int(id))
        product.category = category.key
        product.name = self.request.get('name')
        product.image = self.request.get('pic_url')
        product.intro = self.request.get('intro')
        product.description = self.request.get('description')
        product.review = self.request.get('review')

        # store the data
        product.put()
        self.redirect('/product/' + str(product.key.id()))


class DeleteProduct(webapp2.RequestHandler):
    def post(self, id):
        product = Product.get_by_id(int(id))
        product.key.delete()
        self.redirect('/adminview')


# ===============================================AddCategory=============================================================

class AddCategory(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        addpage = ""
        addcategory = ""
        adminview = ""

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
            if users.is_current_user_admin():
                addpage = "Add Page"
                addcategory = "Add Category"
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

        template = JINJA_ENVIRONMENT.get_template('addcategory.html')
        self.response.write(template.render(template_values))

    def post(self):
        name = self.request.get('category')
        category_query = Categories.query()
        categories = category_query.fetch()
        store_flag = True
        for category1 in categories:
            if category1.name.lower() == name.lower():
                store_flag = False

        if store_flag:
            category = Categories()
            category.name = name
            category.put()
        self.redirect('/add_category')


# ===============================================EditCategory============================================================

class EditCategory(webapp2.RequestHandler):
    def get(self, id):
        user = users.get_current_user()

        addpage = ""
        addcategory = ""
        adminview = ""

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
            if users.is_current_user_admin():
                addpage = "Add Page"
                addcategory = "Add Category"
                adminview = "Admin View"
            else:
                self.redirect('/')

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"
            self.redirect('/')

        category = Categories.get_by_id(int(id))

        category_query = Categories.query()
        categories = category_query.fetch()

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'addpage': addpage,
            'addcategory': addcategory,
            'adminview': adminview,
            'category': category,
            'categories': categories,
            'users': users,
        }

        template = JINJA_ENVIRONMENT.get_template('editcategory.html')
        self.response.write(template.render(template_values))

    def post(self, id):
        name = self.request.get('category')
        category_query = Categories.query()
        categories = category_query.fetch()
        store_flag = True
        for category1 in categories:
            if category1.name.lower() == name.lower():
                store_flag = False

        if store_flag:
            category = Categories.get_by_id(int(id))
            category.name = name
            category.put()
        time.sleep(0.1)
        self.redirect('/add_category')


# ===============================================CategoryDetail==========================================================

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
                addpage = "Add Page"
                addcategory = "Add Category"
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


# ======================================DeleteCategory===================================================================

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
        self.redirect('/add_category')


# =========================================Contact Page==================================================================

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
                addpage = "Add Page"
                addcategory = "Add Category"
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


# ===================================================Policy==============================================================

class Policy(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        addpage = ""
        addcategory = ""
        adminview = ""

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
            if users.is_current_user_admin():
                addpage = "Add Page"
                addcategory = "Add Category"
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

        template = JINJA_ENVIRONMENT.get_template('privacy_policy.html')
        self.response.write(template.render(template_values))


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/add_category', AddCategory),
    (r'/edit_category/(\w+)', EditCategory),
    (r'/category/(\w+)', Category),
    (r'/delete_category/(\w+)', DeleteCategory),
    ('/add_product', AddProduct),
    (r'/edit/(\w+)', EditProduct),
    (r'/delete_product/(\w+)', DeleteProduct),
    ('/admin', AdminPage),
    (r'/product/(\w+)', ProductPage),
    ('/contact', Contact),
    ('/policy', Policy)
], debug=True)
