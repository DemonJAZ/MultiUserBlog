import webapp2
import jinja2
import os
from google.appengine.ext import db
template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape = True)

posts={}

class Handler(webapp2.RequestHandler):
    def write(self , *a ,**kw):
        self.response.out.write(*a, **kw)

    def render_str(self , template , **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))

#DataBase is here
# GQL Entity Declared
class Blog_db(db.Model):
    title = db.StringProperty(required = True)              #Get String (required = neccessary)
    blog_post = db.TextProperty(required = True)
    created_On = db.DateTimeProperty(auto_now_add = True)    #automatically gets date and time from the system
#GQL ENTITY END

class PostBlog(Handler):
    def render_front(self,title,blog,error):
        self.render("posts.html",title=title,blog=blog,error=error)

    def get(self):
        self.render_front(title="",blog="",error="")

    def post(self):
        title = self.request.get("title")
        blog = self.request.get("blog")

        if title and blog:
            a = Blog_db(title=title,blog_post= blog)
            a.put()
            self.redirect("/blog")
        else:
            self.render_front(title,blog,"One or More fields Empty!")

class AllBlogs(Handler):

        def get(self):
            blogs = db.GqlQuery("SELECT * FROM Blog_db ORDER BY created_On DESC")
            self.render("home.html",blogs=blogs)


class MainPage(Handler):
    def render_front(self):
        self.render("home.html")

    def get(self):
        self.render_front()



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newblog', PostBlog),
    ('/blog',AllBlogs)
], debug=True)
