import os
import json
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from CoughClassifier import Classifier
UPLOAD_FOLDER = 'files/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = '39fd2bb12a0cb11544e66997'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def root():
    return '''<!doctype html>
	<body>
	<a href="/forms"> Manual upload </a><br>
	<a href="/upload">upload endpoint</a>
	</body>'''

@app.route('/forms')
def form():
    form='''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post action="/upload" enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''
    return form


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    result=0
    filename=""
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            print("No file part")
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            print("no file selected")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            dst=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(dst)
            result=Classifier(dst)
            #return redirect(url_for('upload_file', name=filename))
    x=dict()
    x["answer"]= result
    x["file"]=filename
    y=json.dumps(x)
    return y
if __name__ == '__main__':
   app.run(port=8080)


