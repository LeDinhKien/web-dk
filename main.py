import os

import time
from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"),
    extensions=['jinja2.ext.autoescape', 'jinja2.ext.loopcontrols'],
    autoescape=True)


class Categories(ndb.Model):
    name = ndb.StringProperty()


class Product(ndb.Model):
    category = ndb.KeyProperty(kind=Categories)
    name = ndb.StringProperty()
    price = ndb.StringProperty()
    sale = ndb.StringProperty(indexed=False)
    sale_price = ndb.FloatProperty(indexed=False, default=0)
    summary = ndb.StringProperty(indexed=False)
    intro = ndb.StringProperty(indexed=False)
    description = ndb.StringProperty(indexed=False)
    thumb = ndb.StringProperty(indexed=False)
    image = ndb.StringProperty(indexed=False)
    review = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


# ===============================================MainPage===============================================================
def render_str(template, **params):
    """
    Render the template with params (dict)
    :param template: template file
    :param params: dictionary of parameter to be rendered
    :return: rendered template to display
    """
    t = JINJA_ENVIRONMENT.get_template(template)
    return t.render(params)


class BaseHandler(webapp2.RequestHandler):
    """
    Parent handler class
    Simplify response methods
    """

    def render(self, template, **kw):
        """
        Display rendered the template with params (dict)
        :param template: template file
        :param kw: dictionary of parameter to be rendered
        :return:
        """
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        """
        Display
        :param a: tuple (format: (x, y, z)) of parameters
        :param kw: key value pair / dict
        :return:
        """
        self.response.out.write(*a, **kw)


class MainPage(BaseHandler):
    def get(self):

        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"

        category_query = Categories.query()
        categories = category_query.fetch()

        # Get the latest products (newest)
        product_query = Product.query().order(-Product.date)
        products = product_query.fetch()

        # Check if there exists a product
        has_product = any(True for product in products if product)

        # Check if there exists a product on sale
        has_sale = any(True for product in products if product.sale)

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'categories': categories,
            'products': products,
            'users': users,
            'has_sale': has_sale,
            'has_product': has_product
        }

        self.render('index.html', **template_values)


# ===============================================AddPage================================================================

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
        list_image.insert(product.thumb, 0)
        product.image = str(list_image).strip('[]')

        if product.sale:
            product.sale_price = float("{0:.2f}".format(float(product.price) * (100 - float(product.sale)) / 100.00))

        if len(product.summary) > 215:
            product.summary = product.summary[:product.summary.rfind(' ', 0, 220)] + '...'

        # store the data
        product.put()
        time.sleep(0.1)
        self.redirect('/product/' + str(product.key.id()))


# ===============================================DetailPage=============================================================

class ProductPage(BaseHandler):
    def get(self, id):
        user = users.get_current_user()

        is_admin = users.is_current_user_admin()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
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

        images = product.image.replace("u'", '').replace("'", '').split(", ")

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'is_admin': is_admin,
            'product': product,
            'products': products,
            'categories': categories,
            'users': users,
            'images': images
        }

        self.render('product.html', **template_values)


# ===============================================EditPage===============================================================

class EditProduct(BaseHandler):
    def get(self, id):
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

        # get category
        category_query = Categories.query()
        categories = category_query.fetch()

        # get product
        product_query = Product.query()
        products = product_query.fetch()

        product = Product.get_by_id(int(id))
        product_key = str(product.key.id())

        images = product.image.replace("u'", '').replace("'", '').split(", ")
        images = images[1:]

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'categories': categories,
            'product': product,
            'products': products,
            'users': users,
            'product_key': product_key,
            'images': images
        }

        self.render('product_edit.html', **template_values)

    def post(self, id):

        # find category and set key
        category_name = self.request.get('category')
        category = Categories.query(Categories.name == category_name).get()

        product = Product.get_by_id(int(id))
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
        # if list_image[0] != product.thumb:
        #     list_image.insert(product.thumb, 0)
        product.image = str(list_image).strip('[]')

        if product.sale:
            product.sale_price = float("{0:.2f}".format(float(product.price) * (100 - float(product.sale)) / 100.00))

        if len(product.summary) > 215:
            product.summary = product.summary[:product.summary.rfind(' ', 0, 220)] + '...'

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

        category_query = Categories.query()
        categories = category_query.fetch()

        product_query = Product.query()
        products = product_query.fetch()

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'categories': categories,
            'products': products,
            'users': users,
        }

        self.render('category_management.html', **template_values)

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

class Category(BaseHandler):
    def get(self, id):
        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
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
            'products': products,
            'categories': categories,
            'users': users,
        }

        self.render('category.html', **template_values)


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

class Contact(BaseHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
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
            'categories': categories,
            'products': products,
            'users': users,
        }

        self.render('contact.html', **template_values)


# ===============================================AdminView==============================================================

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
            'products': products,
            'categories': categories,
            'users': users,
        }

        self.render('adminview.html', **template_values)


# ============================================About Page==============================================================

class About(BaseHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
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
            'categories': categories,
            'products': products,
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

        self.write(form_html)


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
