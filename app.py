import os
from zipfile import ZipFile
from flask import Flask, render_template, request, send_from_directory
from qrcode import make

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'files/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if request.method == 'POST':
        files = request.files.getlist('files')
        for file in files:
            file.save(os.path.join(
                app.config['UPLOAD_FOLDER'], file.filename)) 

        PATH = os.path.join(app.config['UPLOAD_FOLDER'])
        for file in os.listdir(PATH):
            if file != '.gitkeep':
                with open(PATH+file, 'r') as tmp_file:
                    qr = make(tmp_file.read().strip())
                    ext = file.rfind('.')
                    file_name = file[:ext]
                    qr.save(f"{PATH}/{file_name}.png")

        # Convert to zip, delete files and return the zip
        # for file in os.listdir(PATH):
            # if file.endswith('png'):
        return 'Success!'

if __name__ == '__main__':
    app.run(debug=True)
