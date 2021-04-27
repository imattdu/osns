from flask import Blueprint, render_template, request, make_response, jsonify
from flask_cors import cross_origin
from app import db
from models import Note, NoteForward, NoteTag, User

note = Blueprint('note', __name__)


@note.route('/save', methods=['POST'])
@cross_origin(origins='*', supports_credentials=True)
def save_note():
    param_note = request.get_json(silent=True)
    note_tags = param_note.get('tags')
    if param_note.get('id') != None:
        NoteTag.delete_note_tag_by_note_id(param_note.get('id'))
        # 更新操作
        update_note = Note.get_note_by_id(param_note.get('id'))
        update_note.id = param_note.get('id')
        update_note.title = param_note.get('title')
        update_note.content = param_note.get('content')

        Note.update_note(update_note)

        for i in note_tags:
            note_tag = NoteTag.get_note_tag_by_name(i,param_note.get('id'))
            if note_tag == None:
                NoteTag.save(i, param_note.get('id'))
        return make_response('success', 200)
    note = Note()
    note.title = param_note.get('title')
    note.content = param_note.get('content')
    print(param_note.get('tags'))

    note.user_id = param_note.get('user').get('id')

    Note.save_note(note)

    for i in note_tags:
        note_tag = NoteTag.query.filter_by(tag_name=i).first()
        if note_tag == None:
            NoteTag.save(i, note.id)

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



@note.route('/restore/<id>', methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def restore_note(id):
    """恢复笔记"""
    restore_note = Note.query.filter_by(id=id).first()
    restore_note.is_valid = 1
    db.session.add(restore_note)
    db.session.commit()

    note_list = Note.query.filter_by(user_id=restore_note.user_id, is_valid=0).all()
    return jsonify(res_note_list=[i.serialize() for i in note_list])

@note.route('/remove', methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def list_remove_note():
    param_user_id = request.args.get('uid')
    note_list = Note.query.filter_by(user_id=param_user_id, is_valid=0).all()
    return jsonify(res_note_list=[i.serialize() for i in note_list])


@note.route('/list', methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def list_note():
    param_user_id = request.args.get('uid')
    # 先排序后过滤
    note_list = Note.query.order_by(Note.updated_at.desc()).filter(Note.user_id==param_user_id , Note.is_valid == 1)
    print('note_list', note_list)
    res_note_note_tag_list = []
    for note in note_list:
        note_tag_list = NoteTag.query.filter_by(is_valid=1, note_id = note.id).all()
        note = note.serialize()
        res_note_tag_list = []
        for note_tag in note_tag_list:
            res_note_tag_list.append(note_tag.serialize())
        note.setdefault('tags',res_note_tag_list)
        if len(note_tag_list) !=0:
            note.setdefault('tag', note_tag_list[0].tag_name)

        res_note_note_tag_list.append(note)

    return jsonify(res_note_list=[i for i in res_note_note_tag_list])




@note.route('/<id>', methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def get_note_by_id(id):
    note = Note.query.filter_by(id=id).first()
    # NoteTag.

    note_tag_list = NoteTag.query.filter_by(is_valid=1, note_id=id).all()
    note = note.serialize()
    res_note_tag_list = []
    for note_tag in note_tag_list:
        res_note_tag_list.append(note_tag.tag_name)
    note.setdefault('tags', res_note_tag_list)
    print(note)
    return jsonify(note)


@note.route('/forward/save', methods=['POST'])
@cross_origin(origins='*', supports_credentials=True)
def forward_note_by_id():
    param_data = request.get_json(silent=True)
    note_forward = NoteForward()
    note_forward.from_id = param_data.get('from_id')
    note_forward.to_id = param_data.get('to_id')
    note_forward.note_id = param_data.get('noteId')
    note_forward.content = param_data.get('forwardContent')
    db.session.add(note_forward)
    db.session.commit()
    return 'success'


@note.route('/forward/list', methods=['POST'])
@cross_origin(origins='*', supports_credentials=True)
def list_note_forward():
    param_user = request.get_json(silent=True)
    db_note_forward_list = NoteForward.query.filter_by(is_valid=1, to_id=param_user.get('id')).all()

    note_forward_list = []
    for note_forward in db_note_forward_list:
        note_forward = note_forward.serialize()
        note = Note.get_note_by_id(note_forward.get('note_id'))
        note_forward.setdefault('title', note.title)
        user = User.get_user_by_id(note_forward.get('from_id'))
        note_forward.setdefault('username', user.username)
        note_forward.setdefault('user', user.serialize())
        note_forward_list.append(note_forward)


    print(note_forward_list)
    return jsonify(res_note_forward_list=[i for i in note_forward_list])


@note.route('/tag/list', methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def list_note_tag():
    param_user_id = request.args.get('uid')
    note_list = Note.query.filter(Note.user_id == param_user_id and Note.is_valid == 1).order_by(Note.updated_at.desc())
    note_tag_set = set()
    for note in note_list:
        note_tag_list = NoteTag.query.filter_by(is_valid=1, note_id = note.id).all()
        note_tag_set.update(note_tag_list)


    note_tag_name_list = []
    for i in note_tag_set:
        tag_dict = {'text': i.tag_name, 'value': i.tag_name}
        note_tag_name_list.append(tag_dict)
    return jsonify(note_tag_name_list=note_tag_name_list)

