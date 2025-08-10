# main entry point for the application
# this is what gets called when you run "python main.py"
# also what gunicorn imports when it starts the server

from app import my_awesome_app

# export the app instance for gunicorn to find
# gunicorn looks for 'app' by default so we need to provide it
app = my_awesome_app

# only run the dev server if we're executing this file directly
# not when it's imported by gunicorn or other wsgi servers
if __name__ == '__main__':
    print("starting development server...")
    print("visit http://localhost:5000 to see the site!")
    
    # run the flask development server
    # debug=True gives us hot reloading and better error messages
    # host='0.0.0.0' makes it accessible from other devices on network
    my_awesome_app.run(host='0.0.0.0', port=5000, debug=True)
