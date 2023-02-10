import os
from zipfile import ZipFile
from flask import Flask, render_template, request, send_from_directory, jsonify
from qrcode import make

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'files/'
app.config['ZIP_FOLDER'] = 'zip/'


@app.route('/', methods=['GET', 'POST'])
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

        ZIP_PATH = os.path.join(app.config['ZIP_FOLDER']) + 'qr_codes.zip'
        with ZipFile(ZIP_PATH, 'w') as _zip:
            for file in os.listdir(PATH):
                if file != '.gitkeep':
                    if file.endswith('png'):
                        _zip.write(PATH+file)
                    os.remove(PATH+file)

        return ({'result': 'success'}), 201
    elif request.method == 'GET':
        return render_template('index.html')

@app.get('/download')
def download():
    return send_from_directory(
            os.path.join(app.config['ZIP_FOLDER']), 'qr_codes.zip')

if __name__ == '__main__':
    app.run(debug=True)
