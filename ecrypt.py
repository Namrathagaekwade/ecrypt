from flask import Flask, render_template, request, send_file, after_this_request
from werkzeug.utils import secure_filename
import pyAesCrypt
import os
app = Flask(__name__)

uploads_dir = os.path.join(app.instance_path, 'uploads')
download_dir = os.path.join(app.instance_path, 'downloads')
#os.makedirs(uploads_dir,False)
#os.makedirs(download_dir,False)

@app.route('/')
def upload_file():
   return render_template('upload.html')

@app.route('/encrypt', methods = ['POST'])
def uploadenc():
   bufferSize = 64 * 1024
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(uploads_dir,f.filename))
      upload_file = os.path.join(uploads_dir, f.filename)       
      password = request.form['text']
      encfile = f.filename + ".aes"
      download_file = os.path.join(download_dir, encfile)
      pyAesCrypt.encryptFile(upload_file, download_file , password , bufferSize) 
      @after_this_request
      def remove_enc(response):
         os.remove(upload_file)
         os.remove(download_file)
         return response
      return send_file(download_file, as_attachment=True) 

@app.route('/reload', methods = ['POST'])
def reload():
   if request.method == 'POST':
      return render_template('upload.html') 

@app.route('/decrypt', methods = ['POST'])
def uploaddec():
   bufferSize = 64 * 1024
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(uploads_dir,f.filename))
      upload_file = os.path.join(uploads_dir, f.filename)        
      password = request.form['text']
      decfile = f.filename.split('.aes')
      download_file = os.path.join(download_dir,  decfile[0])
      pyAesCrypt.encryptFile(upload_file, download_file , password , bufferSize)  
      @after_this_request
      def remove_dec(response):
         os.remove(upload_file)
         os.remove(download_file)
         return response
      return send_file(download_file, as_attachment=True) 


if __name__ == '__main__':
   app.run(debug = True)
