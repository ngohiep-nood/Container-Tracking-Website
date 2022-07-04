from flask import Blueprint, jsonify, render_template, request, flash, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models import Container, db
import json
import base64
from io import BytesIO
from os import path

baseDir = path.dirname(__file__)
home_api = Blueprint(
    'api', __name__, template_folder=path.join(baseDir, '../templates/home'), url_prefix='/home')


@home_api.route('/', methods=['GET'])
def load_home_page():
    return render_template('home-page.html')

@home_api.route('/search', methods=['POST'])
def search():
    try:
        ids = json.loads(request.form['id_list'])
        resp = []
        for id in ids:
            result = Container.query.filter_by(id=id).first()
            if result is None:
                resp.append({'status': 'error',
                            'message': f'Cannot find container id: {id}',
                             'err_id': id})
                continue
            print(f'owner: {result.user}')
            img1_bytes = BytesIO(result.img_before).getvalue()
            img2_bytes = BytesIO(result.img_after).getvalue()
            img_str1 = "data:image/png;base64," + \
                base64.b64encode(img1_bytes).decode()
            img_str2 = "data:image/png;base64," + \
                base64.b64encode(img2_bytes).decode()

            resp.append({'status': 'success',
                         'id': id,
                         'img_before': img_str1,
                         'img_after': img_str2})

        return json.dumps(resp), 200
    except Exception as e:
        return json.dumps({'status': 'error', 'message': e}), 500


@home_api.route('/upload', methods=['POST', 'GET'])
@jwt_required()
def Upload():
    try:
        if request.method == 'POST':
            user_info = get_jwt_identity()
            if(user_info['isAdmin']):
                ids = request.form.getlist('id')
                files = request.files
                img1 = files.getlist('img1')
                img2 = files.getlist('img2')
                resp = []
                for i in range(len(ids)):
                    id = ids[i]
                    file1 = img1[i]
                    file2 = img2[i]
                    exist_rec = Container.query.get(id)
                    if exist_rec is not None:
                        resp.append({'status': 'error', 
                                    'message': 'container id existed'})
                    else:
                        container = Container(
                            id=id,
                            img_before=file1.read(),
                            img_after=file2.read(),
                            owner_id=user_info['id'])

                        db.session.add(container)
                        db.session.commit()
                        resp.append({'status': 'success',
                                    'message': f'{file1.filename}, {file2.filename} uploaded successfully'})
                return jsonify(resp)
            else:
                return "<h1>Unauthorize!</h1>", 404
    except Exception as e:
        print(e)
        return jsonify({'status': 'error', 'message': e}), 500
