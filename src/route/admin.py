from flask import Blueprint, jsonify, render_template, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services import ContainerService
from os import path
from flasgger import swag_from

baseDir = path.dirname(__file__)
admin = Blueprint(
    'admin', __name__,
    template_folder=path.join(baseDir, '../templates/home'),
    url_prefix='/admin')

@admin.route('/container', methods=['GET'])
@jwt_required()
@swag_from('../docs/admin/get_all_container_id.yaml')
def search_all():
    try:
        user_info = get_jwt_identity()
        if user_info['isAdmin']:
            id = user_info['id']
            resp = ContainerService.get_all_ids_by_owner(id)
            
            return jsonify(resp)
        else:
            return jsonify({
                'status': 'error',
                'message': 'unauthorization'
            }), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': e}), 500

@admin.route('/upload', methods=['GET'])
@jwt_required()
@swag_from('../docs/admin/load_upload_page.yaml')
def load_upload_page():
    user_info = get_jwt_identity()
    if user_info['isAdmin']:
        return render_template('upload-page.html')
    else:
        return jsonify({'status': 'error', 'message': 'unauthorization'}), 500

@admin.route('/upload', methods=['POST'])
@jwt_required()
@swag_from('../docs/admin/upload_container_id.yaml')
def Upload():
    try:
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
                result = ContainerService.upload_container_id(id,
                                                                file1,
                                                                file2,
                                                                user_info['id'])
                resp.append(result)
            return jsonify(resp)
        else:
            return "<h1>Unauthorize!</h1>", 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': e}), 500

@admin.route('/container', methods=['DELETE'])
@jwt_required()
@swag_from('../docs/admin/delete_container_id.yaml')
def DeleteContainerId():
    try:
        user_info = get_jwt_identity()
        if(user_info['isAdmin']):
            res = ContainerService.delete_container_id(request.form.get('id'))
            return res
        else:
            return "<h1>Unauthorize!</h1>", 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': e}), 500

@admin.route('/container', methods=['PUT'])
@jwt_required()
@swag_from('../docs/admin/update_container_id.yaml')
def update_container_info():
    try:
        user_info = get_jwt_identity()
        if user_info['isAdmin']:
            id = request.form.get('id')
            new_img1 = request.files.get('img1')
            new_img2 = request.files.get('img2')
        
            result = ContainerService.update_container_id(id,
                                                        img1=new_img1,
                                                        img2=new_img2)
            return result
        else:
            return "<h1>Unauthorize!</h1>", 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': e}), 500





