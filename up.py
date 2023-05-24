############################
# coding=utf-8
#
# Multi file uploader with Python and Flask
#
# author: cx-4
# date:   01/12/2020
# update: 24/05/2022
# generate ssl cert with:
#  openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -sha256 -nodes -subj "/C=US/ST=Washington/L=Redmond/O=Microsoft Corporation/CN=Microsoft Product Secure Server CA"
#
# execute as root:
#   python ./up.py
#

from flask import Flask
from flask import request
from flask import flash
from flask import redirect
from flask import render_template_string
import os
app = Flask(__name__)
app.secret_key = b'1337'

if (not os.path.exists(os.getcwd()+'/uploads')):
    os.mkdir(os.getcwd()+'/uploads')

@app.route('/')
def idx():
    return 'For file upload go to /upload'

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('no files')
            return redirect(request.url)

        files = request.files.getlist('files[]')
        for f in files:
            if f:
                filename = f.filename
                f.save(os.getcwd() + "/uploads/" + f.filename)

        flash('OK')
        return redirect('/upload')

    if request.method == 'GET':
        return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
        <title>Multi file uploader</title>
        </head>
        <body>
        <h3>select files to upload</h3>
        <p>
            {% with messages = get_flashed_messages() %}
                {% if messages %}
                    <ul class="flashes" style="list-style-type:none;">
                    {% for m in messages %}
                        <li> {{ m }} </li>
                    {% endfor %}
                {% endif %}
            {% endwith %}
        </p>
        <form method="post" action="/upload" enctype="multipart/form-data">
            <dl><p><input type="file" name="files[]" multiple="true" autocomplete="off" required ></p></dl>
            <p><input type="submit" value="Submit" ></p>
        </form>
        </body>
        </html>
        """)
if __name__ == '__main__':
    context = ('cert.pem', 'key.pem')
    app.run(debug=True, ssl_context=context, host='0.0.0.0', port=443)
