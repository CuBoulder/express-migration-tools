import json
import argparse
import sqlalchemy
import pymysql
import phpserialize
import dotenv
import dicttoxml

from lxml import etree
from io import StringIO, BytesIO


def extract_fields(type, id, revision_id):
    # fields = []
    # fci_result = conn.execute(sqlalchemy.text(
    #     f"select a.id, a.field_id, a.field_name, a.entity_type, a.bundle, b.type from field_config_instance a, field_config b where bundle = '{type}' AND a.field_name = b.field_name;"))
    # for fci_item in fci_result:
    #     field = {}
    #     # field['bundle'] = fci_item.bundle
    #     # field['entity_type'] = fci_item.entity_type
    #     field['field_name'] = fci_item.field_name
    #     field['type'] = fci_item.type
    #
    #     fd_result = conn.execute(sqlalchemy.text(
    #         f"select * from field_data_{fci_item.field_name} where bundle = '{type}' AND entity_id = '{id}' AND revision_id = '{revision_id}';"))
    #     data = []
    #     for fd_item in fd_result.mappings():
    #         for col in fd_item:
    #             data.append({'column_name': col, 'value': fd_item[col]})
    #         data = data[7:]
    #
    #     if fci_item.type == 'link_field':
    #         node2 = []
    #         node = {}
    #         for col in data:
    #             node[col['column_name']] = col['value']
    #         node2.append(node)
    #         field['data'] = node2
    #
    #
    #     else:
    #         field['data'] = data

    fields = {}
    fci_result = conn.execute(sqlalchemy.text(
        f"select a.id, a.field_id, a.field_name, a.entity_type, a.bundle, b.type from field_config_instance a, field_config b where bundle = '{type}' AND a.field_name = b.field_name;"))
    for fci_item in fci_result:
        field = {}
        # field['bundle'] = fci_item.bundle
        # field['entity_type'] = fci_item.entity_type
        field['field_name'] = fci_item.field_name
        field['type'] = fci_item.type

        fd_columninfo_result = conn.execute(sqlalchemy.text(f"select * from field_data_{fci_item.field_name} where bundle = '{type}' AND entity_id = '{id}' AND revision_id = '{revision_id}';"))
        columns = []
        for fd_columninfo_item in fd_columninfo_result.mappings():
            for col in fd_columninfo_item:
                columns.append({'column_name': col, 'value': fd_columninfo_item[col]})
            columns = columns[7:]

        columnlist = []
        for column_item in columns:
            columnlist.append(column_item['column_name'])

        columnliststring = ", ".join(columnlist)

        #print(columnliststring)
        if columnliststring == '':
            continue

        data = []

        fd_result = conn.execute(sqlalchemy.text(f"select {columnliststring} from field_data_{fci_item.field_name} where bundle = '{type}' AND entity_id = '{id}' AND revision_id = '{revision_id}';"))

        for fd_item in fd_result.mappings():
            field_item = {}
            for colname in columns:
                field_item[colname['column_name']] = fd_item[colname['column_name']]

            if 'entity_id' in field_item and 'delta' in field_item:
                field_item['id'] = f"{field_item['entity_id']}_{field_item['delta']}"
            data.append(field_item)


        # if len(data) > 0:
        #     fields.append(field)
        field['data'] = data
        fields[field['field_name']] = field

    return fields


engine = sqlalchemy.create_engine("mariadb+pymysql://root:pass@localhost/strategicrelations?charset=utf8mb4", echo=False)

with engine.connect() as conn:

    output = {}

    theme_result = conn.execute(sqlalchemy.text("select value from variable where name = 'theme_default';"))

    for x in theme_result:
        output['theme'] = str(phpserialize.loads(x[0], decode_strings=True))

    filemap = {}
    filemap['images'] = ['image/jpeg', 'image/png']
    filemap['documents'] = ['application/pdf']
    filemap['video'] = []
    filemap['audio'] = []

    files = {}
    files['images'] = []
    files['videos'] = []
    files['audio'] = []
    files['documents'] = []


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

        file['filepath'] = '/home/tirazel/ucb-strategicrelations/files/' + x.uri[9:]

        if x.filemime in filemap['images']:
            files['images'].append(file)
        if x.filemime in filemap['video']:
            files['video'].append(file)
        if x.filemime in filemap['audio']:
            files['audio'].append(file)
        if x.filemime in filemap['documents']:
            files['documents'].append(file)

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

    node_types = {}

    node_result = conn.execute(sqlalchemy.text("select nid, vid, type, title, uid, created, changed from node;"))
    for x in node_result:
        node = {}
        node['nid'] = x.nid
        node['vid'] = x.vid
        node['type'] = x.type
        node['title'] = x.title

        node['fields'] = extract_fields(x.type, x.nid, x.vid)


        layout_result = conn.execute(sqlalchemy.text(f"select layout_id, title, node_type from express_layout WHERE layout_id = '{x.nid}';"))

        for y in layout_result:
            layout = {}
            layout['layout_id'] = y.layout_id
            layout['title']  = y.title
            layout['node_type'] = y.node_type

            layout_field_names = []

            layout_field_names.append('field_footer')
            layout_field_names.append('field_header')
            layout_field_names.append('field_inner_content_left')
            layout_field_names.append('field_inner_content_right')
            layout_field_names.append('field_intro')
            layout_field_names.append('field_sidebar_first')
            layout_field_names.append('field_sidebar_second')
            layout_field_names.append('field_slider')
            layout_field_names.append('field_wide_2')
            layout_field_names.append('field_content_bottom')
            layout_field_names.append('field_post_title')
            layout_field_names.append('field_post_title_wide')

            fields = []

            for lfname in layout_field_names:
                field = {}
                field['name'] = lfname
                field_result = conn.execute(sqlalchemy.text(f"select {lfname}_target_id from field_data_{lfname} WHERE entity_id = '{x.nid}';"))
                for r in field_result:
                    field['target_id'] = r[0]

                    beans = []

                    bean_result = conn.execute(sqlalchemy.text(f"select bid, vid, delta, label, title, type, view_mode, data, uid from bean WHERE bid = '{r[0]}';"))
                    for b in bean_result:

                        bean = {}
                        bean['bid'] = b.bid
                        bean['vid'] = b.vid
                        bean['delta'] = b.delta
                        bean['label'] = b.label
                        bean['title'] = b.title
                        bean['type'] = b.type
                        bean['view_mode'] = b.view_mode
                        bean['data'] = b.data
                        bean['uid'] = b.uid

                        bean_fields = []

                        bean['fields'] = extract_fields(b.type, b.bid, b.vid)

                        beans.append(bean)

                    field['beans'] = beans
                if 'beans' in field:
                    fields.append(field)

            layout['fields'] = fields

            node['layout'] = layout

        if node['type'] not in node_types:
            node_types[node['type']] = []
        node_types[node['type']].append(node)

        #nodes.append(node)
    nodes.append(node_types)
    output['nodes'] = nodes

    vocabularies = {}

    vocabularies_mapping = [
        {'src': 'byline', 'dst': 'byline'},
        {'src': 'department', 'dst': 'department'},
        {'src': 'newsletter', 'dst': 'newsletter'},
        {'src': 'person_type', 'dst': 'ucb_person_job_type'},
        {'src': 'tags', 'dst': 'tags'},
        {'src': 'people_filter_1', 'dst': 'filter_1'},
        {'src': 'people_filter_2', 'dst': 'filter_2'},
        {'src': 'people_filter_3', 'dst': 'filter_3'},
        {'src': 'category', 'dst': 'category'},
        {'src': 'collection_categories', 'dst': ''},
        {'src': 'collection_type', 'dst': ''},
    ]

    for vocab in vocabularies_mapping:
        vocabulary_result = conn.execute(sqlalchemy.text(f"select vid from taxonomy_vocabulary where machine_name='{vocab['src']}';"))
        terms = []
        for vid in vocabulary_result:
            term_result = conn.execute(sqlalchemy.text(f"select name, description, format, weight from taxonomy_term_data WHERE vid = '{vid.vid}';"))
            for t in term_result:
                terms.append({'name': t.name, 'description': t.description, 'format': t.format, 'weight': t.weight})
        vocabularies[vocab['src']] = terms

    #
    # vocabularies_result = conn.execute(sqlalchemy.text(f"select vid, name, machine_name, description, hierarchy, module, weight from taxonomy_vocabulary;"))
    # for x in vocabularies_result:
    #     vocabulary = {}
    #
    #     vocabulary['vid'] = x.vid
    #     vocabulary['name'] = x.name
    #     vocabulary['machine_name'] = x.machine_name
    #     vocabulary['description'] = x.description
    #     vocabulary['hierarchy'] = x.hierarchy
    #     vocabulary['module'] = x.module
    #     vocabulary['weight'] = x.weight
    #
    #     terms = []
    #
    #     term_result = conn.execute(sqlalchemy.text(f"select tid, vid, name, description, format, weight from taxonomy_term_data WHERE vid = '{x.vid}';"))
    #     for y in term_result:
    #         term = {}
    #
    #         term['tid'] = y.tid
    #         term['vid'] = y.vid
    #         term['name'] = y.name
    #         term['description'] = y.description
    #         term['format'] = y.format
    #         term['weight'] = y.weight
    #
    #         terms.append(term)
    #
    #     vocabulary['terms'] = terms
    #
    #     vocabularies.append(vocabulary)

    output['vocabularies'] = vocabularies

    def valid_xml_char_ordinal(c):
        codepoint = ord(c)
        # conditions ordered by presumed frequency
        return (
                0x20 <= codepoint <= 0xD7FF or
                codepoint in (0x9, 0xA, 0xD) or
                0xE000 <= codepoint <= 0xFFFD or
                0x10000 <= codepoint <= 0x10FFFF
        )

    def recurse_xml(root, output):
        if isinstance(output, dict):
            for key in output:
                element = etree.SubElement(root, key)
                recurse_xml(element, output[key])
        if isinstance(output, list):
            for item in output:
                element = etree.SubElement(root, 'item')
                recurse_xml(element, item)
        if isinstance(output, int):
            root.text = str(output)
        if isinstance(output, str):
            cleaned_string = ''.join(c for c in output if valid_xml_char_ordinal(c))
            root.text = cleaned_string






    #print(output)

    root = etree.Element('root')

    recurse_xml(root, output)

    print(etree.tostring(root, pretty_print=True).decode())



    # xml = dicttoxml.dicttoxml(output, attr_type=False, encoding="UTF-8")
    #
    # print(xml)
    #
    # parser = etree.XMLParser(ns_clean=True, recover=True)
    # tree = etree.parse(BytesIO(xml), parser)
    # root = tree.getroot()

    #
    # print(etree.tostring(root, pretty_print=True).decode())


