import os
from threading import Thread
from flask import Flask, request, redirect, flash
from src.ProcessController import process_file



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'your_secret_key'



@app.route("/process", methods=['POST'])
def process():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    filename = file.filename
    if os.path.exists(f"{app.config['UPLOAD_FOLDER']}")== False:
        os.makedirs(f"{app.config['UPLOAD_FOLDER']}")
    file.save(f"{app.config['UPLOAD_FOLDER']}/{filename}")

    #Verarbeite die Datei asynchron
    resultJson =process_file(f"{app.config['UPLOAD_FOLDER']}/{filename}")
    return resultJson

    

if __name__ == '__main__':
    print("Program starten")
    app.run(debug=True)
