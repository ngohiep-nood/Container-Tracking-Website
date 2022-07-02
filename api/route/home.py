from flask import Blueprint, render_template, request, flash
from api.models import Container, db
import json
import base64
from io import BytesIO
from os import path

baseDir = path.dirname(__file__)
home_api = Blueprint('api', __name__, template_folder=path.join(baseDir, '../templates'))

@home_api.route('/welcome')
def welcome():
    return '<h1>🚀Welcome to port project api🚢</h1>'

@home_api.route('/', methods=['GET'])
def load_home_page():
    return render_template('home-page.html')

@home_api.route('/search', methods=['POST'])
def search():
    try:
        id = request.form['id']
        result = Container.query.filter_by(id=id).first()
        if result is None:
            return json.dumps({'status': 'error', 'message': 'Cannot find container id'}), 404
        img1_bytes = BytesIO(result.img_before).getvalue()
        img2_bytes = BytesIO(result.img_after).getvalue()
        img_str1 = "data:image/png;base64," + base64.b64encode(img1_bytes).decode()
        img_str2 = "data:image/png;base64," + base64.b64encode(img2_bytes).decode()

        resp = {'status': 'success',
                'id': id,
                'img_before': img_str1,
                'img_after': img_str2}
        return json.dumps(resp), 200
    except Exception as e:
        return json.dumps({'status': 'error', 'message': e.message}), 500  

@home_api.route('/upload', methods=['POST', 'GET'])
def Upload():
    if request.method == 'POST':
        id = request.form['id']

        exist_rec = Container.query.get(id)
        if exist_rec is not None:
            flash('Container already exists.', category='error')
        else:
            img1 = request.files['img1']
            img2 = request.files['img2']

            container = Container(id=id, img_before=img1.read(), img_after=img2.read())

            db.session.add(container)
            db.session.commit()
            flash('Container successfully uploaded.', category='success')
    return render_template('upload-page.html')
