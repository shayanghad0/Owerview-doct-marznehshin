# my flask app setup - been working on this for a while now
import os
import logging
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

# debug mode is literally my best friend when coding
# shows me exactly what's going wrong instead of just failing silently
logging.basicConfig(level=logging.DEBUG)

# create my flask app instance - pretty straightforward stuff
my_awesome_app = Flask(__name__)

# secret key for sessions and csrf protection and stuff
# learned this lesson after my first app got pwned lol
# always use env vars for secrets kids!
my_awesome_app.secret_key = os.environ.get("SESSION_SECRET", "change-this-or-youll-regret-it-later")

# this proxy middleware thing is super important for deployment
# spent like 2 days debugging https issues before i found this gem
# basically tells flask to trust the proxy headers
my_awesome_app.wsgi_app = ProxyFix(my_awesome_app.wsgi_app, x_proto=1, x_host=1)

# import translation functions to make them available in templates
from translations import get_text, get_current_language, get_doc_text

# make translation functions available in all templates
@my_awesome_app.context_processor
def inject_translation_functions():
    return {
        'get_text': get_text,
        'get_current_language': get_current_language,
        'get_doc_text': get_doc_text
    }

# gotta import routes after creating the app or python throws a fit
# circular imports are the bane of my existence but this works
from routes import *

# only run the dev server if we're running this file directly
# production uses gunicorn instead (much better performance)
if __name__ == '__main__':
    my_awesome_app.run(host='0.0.0.0', port=5000, debug=True)
