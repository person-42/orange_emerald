from flask import jsonify, request, make_response, send_from_directory, abort, render_template, flash, redirect, url_for, session, Flask
import os
from color_api import color_api
app = Flask(__name__)
app.register_blueprint(color_api)
# REMOVE DOCSTRING WHEN FORWARDING TO HOSTING SERVICE
"""app.secret_key=os.environ.get('FLASK_SECRET_KEY')"""
@app.route('/')
def home_page():
    return render_template('home_page.html')
@app.route('/art')
def art():
    return render_template('art.html')
@app.route('/games')
def games():
    return render_template('games.html')
@app.route('/quran')
def quran():
    return render_template('quran.html')
@app.route('/api')
def api():
    return render_template('api.html')
@app.route('/hadith')
def hadith():
    return render_template('hadith.html')
@app.route('/games/paper_minecraft')
def paper_minecraft():
    import paper_mc
    paper_mc.run("some__1")
    return render_template('paper_mc.html')
def run():
    app.run(host="0.0.0.0",port=5000)# Change to port 80 before publishing
if __name__ == '__main__':
    run()
