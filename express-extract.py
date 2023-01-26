import json
import argparse
import sqlalchemy
import pymysql
import phpserialize
import dotenv


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

    users_result = conn.execute(sqlalchemy.text("select uid, name, mail, created, access, login from users;"))
    for x in users_result:
        user = {}
        user['name'] = x[1]
        user['mail'] = x[2]
        user['created'] = x[3]
        user['access'] = x[4]
        user['login'] = x[5]

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

            fd_result = conn.execute(sqlalchemy.text(f"select * from field_data_{y.field_name} where bundle = '{x[2]}';"))
            data = {}
            for z in fd_result.mappings():
                for a in z:
                    data[a] = z[a]
                field['data'] = data
        node['fields'] = fields

        nodes.append(node)

    output['nodes'] = nodes

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
            bean_result = conn.execute(sqlalchemy.text(f"select bid, vid, delta, label, title, type, view_mode, data, uid, created, changed FROM bean WHERE delta = '{x.delta}';"))


        blocks.append(block)
        #express_block_designer
        #express_block_designer_themes
        #express_layout

    output['blocks'] = blocks


    print(json.dumps(output, indent=2))




