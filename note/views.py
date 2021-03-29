from flask import Blueprint, render_template, request, make_response, jsonify
from flask_cors import cross_origin
from app import db
from models import Note, NoteForward

note = Blueprint('note', __name__)


@note.route('/save', methods=['POST'])
@cross_origin(origins='*', supports_credentials=True)
def save_note():
    param_note = request.get_json(silent=True)

    if param_note.get('id') != None:
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


@note.route('/remove/<id>', methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def remove_note_by_id(id):
    remove_note = Note.query.filter_by(id=id).first()
    remove_note.is_valid = 0
    db.session.add(remove_note)
    db.session.commit()
    note_list = Note.query.filter_by(user_id=remove_note.user_id, is_valid=1).all()
    return jsonify(res_note_list=[i.serialize() for i in note_list])


@note.route('/list', methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def list_note():
    param_user_id = request.args.get('uid')
    note_list = Note.query.filter_by(user_id=param_user_id, is_valid=1).all()
    return jsonify(res_note_list=[i.serialize() for i in note_list])


@note.route('/<id>', methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def get_note_by_id(id):
    note = Note.query.filter_by(id=id).first()
    return jsonify(note.serialize())


@note.route('/forward/save', methods=['POST'])
@cross_origin(origins='*', supports_credentials=True)
def forward_note_by_id():
    param_data = request.get_json(silent=True)
    note_forward = NoteForward()
    note_forward.user_id = param_data.get('userId')
    note_forward.note_id = param_data.get('noteId')
    note_forward.content = param_data.get('forwardContent')
    db.session.add(note_forward)
    db.session.commit()
    print(param_data)
    return 'success'


@note.route('/forward/list', methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def list_note_forward():
    db_note_forward_list = NoteForward.query.filter_by(is_valid=1).all()
    print(db_note_forward_list)
    note_forward_list = []
    for note_forward in db_note_forward_list:
        note_forward = note_forward.serialize()
        note = Note.get_note_by_id(note_forward.get('note_id'))
        note_forward.setdefault('title', note.title)
        note_forward_list.append(note_forward)

    print(note_forward_list)
    return jsonify(res_note_forward_list=[i for i in note_forward_list])
