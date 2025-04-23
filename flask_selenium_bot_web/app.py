from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from bot_runner import run_bot

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print("تم حفظ الملف بنجاح في:", filepath)
        print("محتويات مجلد uploads:", os.listdir(app.config['UPLOAD_FOLDER']))
        try:
            result = run_bot(filepath)
            return result
        except Exception as e:
            return str(e), 500
    return 'الملف غير صحيح. يرجى رفع ملف Excel صحيح.'

if __name__ == '__main__':
    app.run(debug=True)
