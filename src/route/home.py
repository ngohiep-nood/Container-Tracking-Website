from flask import Blueprint, jsonify, render_template, request
from src.services import ContainerService
from os import path
from flasgger import swag_from

baseDir = path.dirname(__file__)
home_api = Blueprint(
    'api', __name__,
    template_folder=path.join(baseDir, '../templates/home'),
    url_prefix='/home')

@home_api.route('/', methods=['GET'])
@swag_from('../docs/home/load_search_page.yaml')
def load_home_page():
    return render_template('home-page.html')

@home_api.route('/search', methods=['POST'])
@swag_from('../docs/home/search.yaml')
def search():
    try:
        ids = request.form['id_list'].split(',')
        resp = []
        for id in ids:
            result = ContainerService.get_container_by_id(id)

            if result is None:
                resp.append({'status': 'error',
                            'message': f'Cannot find container id: {id}',
                             'err_id': id})
                continue

            resp.append({'status': 'success',
                         'id': result['id'],
                         'img_before': result['img1'],
                         'img_after': result['img2'],
                         'owner': result['owner']})
        # return 'success'
        return jsonify(resp), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': e}), 500

