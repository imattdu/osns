from flask import Blueprint, render_template, request, make_response, jsonify
from flask_cors import cross_origin
from app import db
from models import Note, NoteForward, NoteTag, User, NoteAndNoteTag

note = Blueprint('note', __name__)


@note.route('/save', methods=['POST'])
@cross_origin(origins='*', supports_credentials=True)
def save_note():
    param_note = request.get_json(silent=True)
    param_note_tags = param_note.get('tags')
    param_user = param_note.get('user')

    note = Note(title=param_note.get('title'),
                content=param_note.get('content'),
                user_id=param_user.get('id'))
    print(param_note.get('id'), -1)
    if param_note.get('id') != -1:
        note = Note.get_note_by_id(param_note.get('id'))
        note.title = param_note.get('title'),
        note.content = param_note.get('content'),
        note.user_id = param_user.get('id')

    Note.save_note(note)

    # NoteAndNoteTag.list_note_and_note_tag_by_note_id(note.id)

    if len(param_note_tags) != 0:
        data_note_tags = NoteTag.list_note_tag_by_user_id(param_user.get('id'))
        print(data_note_tags)
        data_note_tags_value = []
        for i in data_note_tags:
            # data_note_tags data_note_tags data_note_tags
            data_note_tags_value.append(i.tag_name)
        print(data_note_tags_value)

        for i in param_note_tags:
            if i in data_note_tags_value:
                continue
            NoteTag.save(i, param_user.get('id'))
        note_and_note_tag_list = NoteAndNoteTag.list_note_and_note_tag_by_note_id(note.id)
        for i in note_and_note_tag_list:
            i.is_valid = 0
            NoteAndNoteTag.save_note_and_note_tag(i)
        for i in param_note_tags:
            note_tag = NoteTag.get_note_tag_by_name(i, param_user.get('id'))
            note_and_note_tag = NoteAndNoteTag(note.id, note_tag.id)
            NoteAndNoteTag.save_note_and_note_tag(note_and_note_tag)
    else:
        note_and_note_tags = NoteAndNoteTag.list_note_and_note_tag_by_note_id(note.id)
        for i in note_and_note_tags:
            i.is_valid = 0
            NoteAndNoteTag.save_note_and_note_tag(i)

    return ''



def save_note_test():
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

@note.route('/remove/forever/<id>', methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def remove_note_forever(id):
    """永久删除"""
    restore_note = Note.query.filter_by(id=id).first()
    restore_note.is_valid = 9
    db.session.add(restore_note)
    db.session.commit()

    note_list = Note.query.filter_by(user_id=restore_note.user_id, is_valid=0).all()
    return jsonify(res_note_list=[i.serialize() for i in note_list])


@note.route('/remove', methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def list_remove_note():
    param_user_id = request.args.get('uid')
    param_cur_page = request.args.get('curPage')
    param_page_size = request.args.get('pageSize')

    if param_cur_page == None:
        param_cur_page = 1
    else:
        param_cur_page = int(request.args.get('curPage'))

    if param_page_size == None:
        param_page_size = 5
    else:
        param_page_size = int(request.args.get('pageSize'))
    param_tags = request.args.get('tags')
    note_list = Note.query.filter_by(user_id=param_user_id, is_valid=0).all()

    note_list = list(note_list)
    note_list_size = len(note_list)
    start = (param_cur_page - 1) * param_page_size
    end = param_cur_page * param_page_size
    note_list = note_list[start:end]
    res_note_list = [i.serialize() for i in note_list]
    res_data = {'res_note_list': res_note_list, 'total': note_list_size}

    return res_data


@note.route('/list', methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def list_note():
    param_user_id = request.args.get('uid')
    param_cur_page = request.args.get('curPage')
    param_page_size = request.args.get('pageSize')

    if param_cur_page == None:
        param_cur_page = 1
    else:
        param_cur_page = int(request.args.get('curPage'))

    if param_page_size == None:
        param_page_size = 5
    else:
        param_page_size = int(request.args.get('pageSize'))
    param_tags = request.args.get('tags')

    if param_tags != None and len(param_tags) != 0:
        param_tags = param_tags.split(',')
        note_list = list_note_by_condition(param_user_id, param_tags)
    else:
        # 先排序后过滤
        note_list = Note.query.order_by(Note.updated_at.desc()).filter(Note.user_id == param_user_id,
                                                                       Note.is_valid == 1)
        print('note_list', note_list)

    note_list = list(note_list)
    note_list_size = len(note_list)
    start = (param_cur_page - 1) * param_page_size
    end = param_cur_page * param_page_size
    note_list = note_list[start:end]
    res_note_list = [i.serialize() for i in note_list]
    res_data = {'res_note_list': res_note_list, 'total': note_list_size}

    return res_data



# @note.route('/list/condition', methods=['POST'])
# @cross_origin(origins='*', supports_credentials=True)
def list_note_by_condition(param_user_id, param_tags):
    # param_data = request.get_json(silent=True)
    # param_user_id = param_data.get('uid')
    # param_tags = param_data.get('tags')

    note_tag_id_list = []
    for i in param_tags:
        note_tag = NoteTag.get_note_tag_by_name(i, param_user_id)
        if note_tag == None:
            continue
        note_tag_id_list.append(note_tag.id)

    note_id_set = set()
    for i in note_tag_id_list:
        note_and_note_tags = NoteAndNoteTag.list_note_and_note_tag_by_note_tag_id(i)
        for j in note_and_note_tags:
            note_id_set.add(j.note_id)

    # 先排序后过滤
    note_list = []
    for i in note_id_set:
        note = Note.get_note_by_id(i)
        note_list.append(note)
    # note_list = Note.query.order_by(Note.updated_at.desc()).filter(Note.user_id==param_user_id , Note.is_valid == 1)
    print('note_list', note_list)


    return note_list


@note.route('/<id>', methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def get_note_by_id(id):
    note = Note.query.filter_by(id=id).first()
    # NoteTag
    note_and_note_tags = NoteAndNoteTag.list_note_and_note_tag_by_note_id(id)
    res_note = []
    for i in note_and_note_tags:
        note_tag_id = i.note_tag_id
        note_tag = NoteTag.get_note_tag_by_id(note_tag_id)
        res_note.append(note_tag.tag_name)

    note = note.serialize()
    note['tags'] = res_note
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


@note.route('/forward/list', methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def list_note_forward():
    param_user_id = request.args.get('uid')
    param_cur_page = request.args.get('curPage')
    param_page_size = request.args.get('pageSize')

    if param_cur_page == None:
        param_cur_page = 1
    else:
        param_cur_page = int(request.args.get('curPage'))

    if param_page_size == None:
        param_page_size = 5
    else:
        param_page_size = int(request.args.get('pageSize'))

    db_note_forward_list = NoteForward.query.filter_by(is_valid=1, to_id=param_user_id).all()

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

    note_forward_list = list(note_forward_list)
    note_forward_list_size = len(note_forward_list)
    start = (param_cur_page - 1) * param_page_size
    end = param_cur_page * param_page_size
    note_forward_list = note_forward_list[start:end]

    res_data = {'res_note_forward_list': note_forward_list, 'total': note_forward_list_size}

    return res_data


# @note.route('/tag', methods=['PUT'])
# @cross_origin(origins='*', supports_credentials=True)
def save_note_tags():
    param_data = request.get_json(silent=True)
    uid = param_data.get('uid')
    tags = param_data.get('tags')
    for i in tags:
        note_tag = NoteTag.get_note_tag_by_name(tag_name=i, user_id=uid)
        if note_tag !=None:
            note_and_note_tags = NoteAndNoteTag.list_note_and_note_tag_by_note_tag_id(note_tag.id)
            for j in note_and_note_tags:
                j.is_valid = 0
                NoteAndNoteTag.save_note_and_note_tag(j)
            note_tag.is_valid = 0
            NoteTag.save_obj(note_tag)

        NoteTag.save(tag_name=i, user_id=uid)
    return ''

@note.route('/tag', methods=['PUT'])
@cross_origin(origins='*', supports_credentials=True)
def save_note_tag_by_tag_name():
    param_data = request.get_json(silent=True)
    uid = param_data.get('uid')
    tag_name = param_data.get('tag')
    NoteTag.save(tag_name=tag_name, user_id=uid)
    return ''


@note.route('/tag', methods=['DELETE'])
@cross_origin(origins='*', supports_credentials=True)
def delete_note_tag_by_tag_name():

    uid = request.args.get('uid')
    tag_name = request.args.get('tag')
    note_tag = NoteTag.get_note_tag_by_name(tag_name=tag_name, user_id=uid)
    if note_tag != None:
        note_and_note_tags = NoteAndNoteTag.list_note_and_note_tag_by_note_tag_id(note_tag.id)
        for i in note_and_note_tags:
            i.is_valid = 0
            NoteAndNoteTag.save_note_and_note_tag(i)
        note_tag.is_valid = 0
        NoteTag.save_obj(note_tag)
    return ''



@note.route('/tag/list', methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def list_note_tag():
    param_user_id = request.args.get('uid')
    # note_list = Note.query.filter(Note.user_id == param_user_id and Note.is_valid == 1).order_by(Note.updated_at.desc())
    # note_tag_set = set()
    # for note in note_list:
    #     note_tag_list = NoteTag.query.filter_by(is_valid=1, note_id = note.id).all()
    #     note_tag_set.update(note_tag_list)
    # note_tag_name_list = []
    # for i in note_tag_set:
    #     tag_dict = {'text': i.tag_name, 'value': i.tag_name}
    #     note_tag_name_list.append(tag_dict)
    note_tag_list = NoteTag.list_note_tag_by_user_id(param_user_id)
    note_tag_name_list = []
    for i in note_tag_list:
        tag_dict = {'value': i.tag_name, 'label': i.tag_name}
        note_tag_name_list.append(tag_dict)
    return jsonify(note_tag_name_list=note_tag_name_list)

