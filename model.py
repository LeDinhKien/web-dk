import os

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


class BaseHandler(webapp2.RequestHandler):
    """
    Parent handler class
    Simplify response methods and common methods
    """

    def render_str(self, template, **params):
        """
        Render the template with params (dict)
        :param t: template file
        :param params: dictionary of parameter to be rendered
        :return: rendered template to display
        """
        t = JINJA_ENVIRONMENT.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        """
        Display rendered the template with params (dict)
        :param template: template file
        :param kw: dictionary of parameter to be rendered
        :return:
        """
        self.response.out.write(self.render_str(template, **kw))

    def write(self, *a, **kw):
        """
        Display
        :param a: tuple (format: (x, y, z)) of parameters
        :param kw: key value pair / dict
        :return:
        """
        self.response.out.write(*a, **kw)


def get_products():
    """
    Get all products
    :return: a list of products sorted by date added (desc)
    """
    product_query = Product.query().order(-Product.date)
    products = product_query.fetch()
    return products


def get_categories():
    """
    Get all categories
    :return: a list of categories
    """
    category_query = Categories.query()
    categories = category_query.fetch()
    return categories


def exist_category(name):
    """
    Check if there exists a category with the same name
    :param name: new name to compare
    :return: True if exists, False otherwise
    """
    return any(True for category in get_categories() if category.name == name)


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
