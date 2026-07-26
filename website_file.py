from flask import jsonify, request, make_response, send_from_directory, abort, render_template, flash, redirect, url_for, session, Flask
app = Flask(__name__)
@app.route('/')
def home_page():
    pass
