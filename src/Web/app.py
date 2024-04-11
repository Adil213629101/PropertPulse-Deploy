from flask import Flask, render_template
from flask_cors import CORS, cross_origin
from fastapi.middleware.cors import CORSMiddleware
import flask_cors
app = Flask(__name__, static_folder='assets')
cors = CORS(app)



@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/realtor-scraper')
def realtor():
    return render_template('realtor.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')


@app.route('/docs')
def docs():
    return render_template('docs.html')


@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/test')
def test():
    return render_template('test.html')


if __name__ == '__main__':
    app.run(debug=True)