from flask import Blueprint, render_template, request, make_response, jsonify
from flask_cors import cross_origin
from app import db
from models import Note

note = Blueprint('note', __name__)


@note.route('/save', methods=['POST'])
@cross_origin(origins='*', supports_credentials=True)
def save_note():
    param_note = request.get_json(silent=True)

    if param_note.get('id') != -1:
        print('hello word')
        # 更新操作
        update_note = Note.query.filter_by(id=param_note.get('id')).first()
        update_note.id = param_note.get('id')
        update_note.title = param_note.get('title')
        update_note.content = param_note.get('content')
        db.session.add(update_note)
        db.session.commit()
        return make_response('success', 200)
    note = Note()
    note.title = param_note.get('title')
    note.content = param_note.get('content')
    note.user_id = param_note.get('user').get('id')
    print(param_note)

    db.session.add(note)
    db.session.commit()
    return make_response('success', 200)


@note.route('/list', methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def list_note():
    param_user_id = request.args.get('uid')
    note_list = Note.query.filter_by(user_id=param_user_id).all()
    return jsonify(res_note_list = [i.serialize() for i in note_list])


@note.route('/<id>', methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def get_note_by_id(id):

    note = Note.query.filter_by(id=id).first()
    return jsonify(note.serialize())
