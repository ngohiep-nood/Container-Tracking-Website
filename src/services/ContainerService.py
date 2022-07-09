from src.models import Container, db
import base64
from io import BytesIO

def get_all_ids_by_owner(owner_id):
    ids = Container.query.filter_by(owner_id=owner_id).all()
    resp = []
    print(ids)
    for id in ids:
        img1_bytes = BytesIO(id.img_before).getvalue()
        img2_bytes = BytesIO(id.img_after).getvalue()
        img_str1 = "data:image/png;base64," + \
            base64.b64encode(img1_bytes).decode()
        img_str2 = "data:image/png;base64," + \
            base64.b64encode(img2_bytes).decode()
        resp.append({
            'id': id.id,
            'img1': img_str1,
            'img2': img_str2,
            'owner': id.user.username
        })
    return resp

def get_container_by_id(id):
    resp = Container.query.get(id)
    if(resp == None):
        return None

    print(f'id: {id} | owner: {resp.user}')
    img1_bytes = BytesIO(resp.img_before).getvalue()
    img2_bytes = BytesIO(resp.img_after).getvalue()
    img_str1 = "data:image/png;base64," + \
        base64.b64encode(img1_bytes).decode()
    img_str2 = "data:image/png;base64," + \
        base64.b64encode(img2_bytes).decode()
    return {
        'id': id,
        'img1': img_str1,
        'img2': img_str2,
        'owner': resp.user.username
    }


def upload_container_id(id, img_before, img_after, owner_id):
    exist_id = Container.query.get(id)
    if exist_id is None:
        new_id = Container(id=id,
                           img_before=img_before.read(),
                           img_after=img_after.read(),
                           owner_id=owner_id)

        db.session.add(new_id)
        db.session.commit()
        return {'status': 'success',
                'message': f'{img_before.filename}, {img_after.filename} uploaded successfully'}
    return {
        'status': 'error',
        'message': 'container id existed!'
    }


def delete_container_id(id):
    exist_id = Container.query.get(id)
    if exist_id is None:
        return {
            'status': 'error',
            'message': 'container id does not exist'
        }

    db.session.delete(exist_id)
    db.session.commit()

    return {
        'status': 'success',
        'message': f'id {id} deleted'
    }


def update_container_id(id, **args):
    # print(id)
    container_id = Container.query.get(id)

    if container_id is None:
        return {
            'status': 'error',
            'message': 'container id does not exist'
        }

    new_img1 = args.get('img1')
    new_img2 = args.get('img2')

    if new_img1 is not None:
        container_id.img_before = new_img1.read()
    if new_img2 is not None:
        container_id.img_after = new_img2.read()

    db.session.commit()

    return {
        'status': 'success',
        'message': 'container id is updated!'
    }
