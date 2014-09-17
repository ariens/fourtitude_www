#!flask/bin/python

# Deprecated when running via uwsgi and nginx

from fourtitude import app
if __name__ == "__main__":
    app.run(host='localhost', debug=True)
