import json
import argparse
import sqlalchemy
import pymysql
import phpserialize
import dotenv
import dicttoxml

from lxml import etree
from io import StringIO, BytesIO


engine = sqlalchemy.create_engine("mariadb+pymysql://root:pass@localhost/strategicrelations?charset=utf8mb4", echo=False)

with engine.connect() as conn:

    output = {}

    theme_result = conn.execute(sqlalchemy.text("select value from variable where name = 'theme_default';"))

    for x in theme_result:
        output['theme'] = str(phpserialize.loads(x[0], decode_strings=True))


    files = []
    files_result = conn.execute(sqlalchemy.text("select fid, uid, filename, uri, filemime, filesize, status, timestamp, type from file_managed;"))
    for x in files_result:
        file = {}
        file['fid'] = x.fid
        file['uid'] = x.uid
        file['filename'] = x.filename
        file['uri'] = x.uri
        file['filemime'] = x.filemime
        file['filesize'] = x.filesize
        file['status'] = x.status
        file['timestamp'] = x.timestamp
        file['type'] = x.type
        files.append(file)

    output['files'] = files

    users = []

    users_result = conn.execute(sqlalchemy.text("select uid, name, mail, created, access, login, status from users;"))
    for x in users_result:

        skiplist = []
        skiplist.append('alco6164')
        skiplist.append('mibo7729')
        skiplist.append('jesp3304')
        skiplist.append('fraziere')
        skiplist.append('jesp3304')
        skiplist.append('wetu1300')
        skiplist.append('linebarg')
        skiplist.append('brokaw')
        skiplist.append('crafts')
        skiplist.append('')

        if x[1] in skiplist or x[0] == 1:
            continue

        user = {}
        user['uid'] = x[0]
        user['name'] = x[1]
        user['mail'] = x[2]
        user['created'] = x[3]
        user['access'] = x[4]
        user['login'] = x[5]
        user['status'] = x[6]

        roles = []

        roles_result = conn.execute(sqlalchemy.text(f"select r.name from users u, users_roles ur, role r WHERE u.uid = ur.uid AND ur.rid = r.rid AND u.uid = '{x[0]}';"))
        for y in roles_result:
            roles.append(y[0])

        user['roles'] = roles
        users.append(user)
    output['users'] = users

    nodes = []

    node_result = conn.execute(sqlalchemy.text("select nid, vid, type, title, uid, created, changed from node;"))
    for x in node_result:
        node = {}
        node['type'] = x[2]
        node['title'] = x[3]

        fields = []
        fci_result = conn.execute(sqlalchemy.text(f"select id, field_id, field_name, entity_type, bundle from field_config_instance where bundle = '{x[2]}';"))
        for y in fci_result:
            field = {}
            field['bundle'] = y.bundle
            field['entity_type'] = y.entity_type
            field['field_name'] = y.field_name
            fields.append(field)

            fd_result = conn.execute(sqlalchemy.text(f"select * from field_data_{y.field_name} where bundle = '{x[2]}' AND entity_id = '{x[0]}' AND revision_id = '{x[1]}';"))
            data = {}
            for z in fd_result.mappings():
                for a in z:
                    data[a] = z[a]
                field['data'] = data
        node['fields'] = fields

        nodes.append(node)

    output['nodes'] = nodes

    vocabularies = []

    vocabularies_result = conn.execute(sqlalchemy.text(f"select vid, name, machine_name, description, hierarchy, module, weight from taxonomy_vocabulary;"))
    for x in vocabularies_result:
        vocabulary = {}

        vocabulary['vid'] = x.vid
        vocabulary['name'] = x.name
        vocabulary['machine_name'] = x.machine_name
        vocabulary['description'] = x.description
        vocabulary['hierarchy'] = x.hierarchy
        vocabulary['module'] = x.module
        vocabulary['weight'] = x.weight

        terms = []

        term_result = conn.execute(sqlalchemy.text(f"select tid, vid, name, description, format, weight from taxonomy_term_data WHERE vid = '{x.vid}';"))
        for y in term_result:
            term = {}

            term['tid'] = y.tid
            term['vid'] = y.vid
            term['name'] = y.name
            term['description'] = y.description
            term['format'] = y.format
            term['weight'] = y.weight

            terms.append(term)

        vocabulary['terms'] = terms

        vocabularies.append(vocabulary)

    output['vocabularies'] = vocabularies

    blocks = []

    block_result = conn.execute(sqlalchemy.text(f"select bid, module, delta, theme, status, weight, region, custom, visibility, pages, title, cache from block WHERE theme = '{output['theme']}';"))

    for x in block_result:
        block = {}
        block['module'] = x.module
        block['delta'] = x.delta
        block['theme'] = x.theme
        block['status'] = x.status
        block['weight'] = x.weight
        block['region'] = x.region
        block['custom'] = x.custom
        block['visibility'] = x.visibility
        block['pages'] = x.pages
        block['title'] = x.title
        block['cache'] = x.cache

        if x.module == 'bean':
            beans = []
            bean_result = conn.execute(sqlalchemy.text(f"select bid, vid, delta, label, title, type, view_mode, data, uid, created, changed FROM bean WHERE delta = '{x.delta}';"))
            for y in bean_result:
                bean = {}

                bean['bid'] = y.bid
                bean['vid'] = y.vid
                bean['delta'] = y.delta
                bean['label'] = y.label
                bean['title'] = y.title
                bean['type'] = y.type
                bean['view_mode'] = y.view_mode
                bean['data'] = y.data
                bean['uid'] = y.uid
                bean['created'] = y.created
                bean['changed'] = y.changed

                beans.append(bean)
            block['bean'] = bean

        #blocks.append(block)
        #express_block_designer
        #express_block_designer_themes
        #express_layout

    #output['blocks'] = blocks


    #print(json.dumps(output, indent=2))
    xml = dicttoxml.dicttoxml(output, attr_type=False, encoding="UTF-8")

    parser = etree.XMLParser(ns_clean=True, recover=True)
    tree = etree.parse(BytesIO(xml), parser)
    root = tree.getroot()


    print(etree.tostring(root, pretty_print=True).decode())


