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


def remove_empty(thumb, alist):
    """
    Remove empty string in a list. Use for image urls
    :param thumb: product thumbnail, add when there is no image url
    :param alist: list of urls
    :return:
    """
    if u'' in alist:
        alist[:] = (x for x in alist if x != u'')
    if len(alist) == 0:
        alist.insert(0, thumb)


def calculate_sale(price, sale):
    """
    Calculate the sale price
    :param price: the original price
    :param sale: the sale percentage
    :return: sale price
    """
    return float("{0:.2f}".format(float(price) * (100 - float(sale)) / 100.00))


class Categories(ndb.Model):
    name = ndb.StringProperty()


class Product(ndb.Model):
    category = ndb.KeyProperty(kind=Categories)
    name = ndb.StringProperty(indexed=False)
    price = ndb.StringProperty(indexed=False)
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
    Simplify response methods and common methods
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

    def get_products(self):
        """
        Get all products
        :return: a list of products sorted by date added (desc)
        """
        product_query = Product.query().order(-Product.date)
        products = product_query.fetch()
        return products

    def get_categories(self):
        """
        Get all categories
        :return: a list of categories
        """
        category_query = Categories.query()
        categories = category_query.fetch()
        return categories

    def exist_category(self, name):
        """
        Check if there exists a category with the same name
        :param name: new name to compare
        :return: True if exists, False otherwise
        """
        return any(True for category in self.get_categories() if category.name == name)


class MainPage(BaseHandler):
    def get(self):

        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"

        products = self.get_products()

        # Check if there exists a product
        has_product = any(True for product in products if product)

        # Check if there exists a product on sale
        has_sale = any(True for product in products if product.sale)

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'categories': self.get_categories(),
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

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'categories': self.get_categories(),
            'products': self.get_products(),
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


# ===============================================DetailPage=============================================================

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
            'categories': self.get_categories(),
            'products': self.get_products(),
            'users': users,
            'images': images
        }

        self.render('product.html', **template_values)


# ===============================================EditPage===============================================================

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
            'categories': self.get_categories(),
            'products': self.get_products(),
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


# ===============================================DeleteProduct==========================================================

class DeleteProduct(webapp2.RequestHandler):
    def post(self, product_id):
        product = Product.get_by_id(int(product_id))
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

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'categories': self.get_categories(),
            'products': self.get_products(),
            'users': users,
        }

        self.render('category_management.html', **template_values)

    def post(self):  # Add category
        name = self.request.get('category')

        # If not existed, change name
        if not self.exist_category(name):
            category = Categories()
            category.name = name
            category.put()

        time.sleep(0.1)
        self.redirect('/manage_category')


# ===============================================EditCategory===========================================================

class EditCategory(BaseHandler):
    def post(self, category_id):
        name = self.request.get('category')
        category = Categories.get_by_id(int(category_id))

        # If not existed, change name
        if not self.exist_category(name):
            category.name = name
            category.put()

        time.sleep(0.1)
        self.redirect('/manage_category')


# ===============================================CategoryDetail=========================================================

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
            'categories': self.get_categories(),
            'products': self.get_products(),
            'users': users,
        }

        self.render('category.html', **template_values)


# =============================================DeleteCategory===========================================================

class DeleteCategory(BaseHandler):
    def post(self, category_id):
        category = Categories.get_by_id(int(category_id))

        # Delete all products in the category then delete the category
        for product in self.get_products():
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

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'categories': self.get_categories(),
            'products': self.get_products(),
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

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'categories': self.get_categories(),
            'products': self.get_products(),
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

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'categories': self.get_categories(),
            'products': self.get_products(),
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
