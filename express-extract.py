import json
import argparse
import sqlalchemy
import pymysql
import phpserialize
import dotenv
import dicttoxml
import time
import re

from lxml import etree
from io import StringIO, BytesIO

def extract_subfields(field):
    fd_columninfo_result = conn.execute(sqlalchemy.text(f"select column_name as 'subfield' from information_schema.COLUMNS where table_schema = DATABASE() AND table_name = 'field_data_{field}' limit 100 offset 7;"))
    subfields = []
    subfields.append('entity_id')
    subfields.append('delta')
    for item in fd_columninfo_result:
        subfields.append(item.subfield)
    return subfields


def extract_fields(type, id, revision_id):


    fields = {}
    fci_result = conn.execute(sqlalchemy.text(f"select a.id, a.field_id, a.field_name, a.entity_type, a.bundle, b.type from field_config_instance a, field_config b where bundle = '{type}' AND a.field_name = b.field_name;"))
    for fci_item in fci_result:
        field = {}
        # field['bundle'] = fci_item.bundle
        # field['entity_type'] = fci_item.entity_type
        field['field_name'] = fci_item.field_name
        field['type'] = fci_item.type


        columns = extract_subfields(fci_item.field_name)

        data = []

        fd_result = conn.execute(sqlalchemy.text(f"select {', '.join(columns)} from field_data_{fci_item.field_name} where bundle = '{type}' AND entity_id = '{id}' AND revision_id = '{revision_id}';"))

        for fd_item in fd_result.mappings():
            field_item = {}
            for colname in columns:
                field_item[colname] = fd_item[colname]

            if 'entity_id' in field_item and 'delta' in field_item:
                field_item['id'] = f"{field_item['entity_id']}_{field_item['delta']}"
            data.append(field_item)

        field['data'] = data
        fields[field['field_name']] = field

    return fields


engine = sqlalchemy.create_engine("mariadb+pymysql://root:pass@localhost/strategicrelations?charset=utf8mb4", echo=False)

with engine.connect() as conn:

    output = {}

    theme_result = conn.execute(sqlalchemy.text("select value from variable where name = 'theme_default';"))

    for x in theme_result:
        output['theme'] = str(phpserialize.loads(x[0], decode_strings=True))

    # Extract url_alias table
    urlaliasmap = {}
    urlalias_result = conn.execute(sqlalchemy.text("select source, alias from url_alias;"))
    for x in urlalias_result:
        urlaliasmap[x.source] = x.alias

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

        file['filepath'] = '/home/tirazel/Projects/migration-tools/ucb-strategicrelations/files/' + x.uri[9:]

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

    node_result = conn.execute(sqlalchemy.text("select nid, vid, type, title, uid, status, created, changed, comment, promote, sticky from node;"))
    for x in node_result:
        node = {}
        node['nid'] = x.nid
        node['vid'] = x.vid
        node['type'] = x.type
        node['title'] = x.title
        node['uid'] = x.uid
        node['status'] = x.status
        node['created'] = x.created
        node['changed'] = x.changed
        node['comment'] = x.comment
        node['promote'] = x.promote
        node['sticky'] = x.sticky


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

    # Menus
    menumap = {}
    menumap['main-menu'] = 'main'
    menumap['menu-footer-menu'] = 'footer'
    menumap['menu-secondary-menu'] = 'secondary'

    menusignore = []
    menusignore.append('management')
    menusignore.append('navigation')
    menusignore.append('user-menu')


    menus = []
    menu_result = conn.execute(sqlalchemy.text("select menu_name, title, description from menu_custom;"))
    for x in menu_result:
        menu = {}

        if x.menu_name in menusignore:
            continue


        menu['name'] = x.menu_name
        menu['title'] = x.title
        menu['desciption'] = x.description
        menu['links'] = []

        menulink_result = conn.execute(sqlalchemy.text(f"select menu_name, mlid, plid, link_path, router_path, link_title, options, hidden, external, has_children, expanded, weight, depth, customized, p1, p2, p3, p4, p5, p6, p7, p8, p9, updated from menu_links WHERE menu_name = '{x.menu_name}';"))
        for y in menulink_result:
            menulink = {}

            if y.menu_name in menumap:
                menulink['menu_name'] = menumap[y.menu_name]
            else:
                menulink['menu_name'] = y.menu_name

            menulink['mlid'] = y.mlid
            menulink['plid'] = y.plid

            if y.link_path in urlaliasmap:
                menulink['link_path'] = urlaliasmap[y.link_path]
            else:
                menulink['link_path'] = y.link_path


            menulink['router_path'] = y.router_path
            menulink['link_title'] = y.link_title
            menulink['options'] = y.options
            menulink['hidden'] = y.hidden
            menulink['external'] = y.external
            menulink['has_children'] = y.has_children
            menulink['expanded'] = y.expanded
            menulink['weight'] = y.weight
            menulink['depth'] = y.depth
            menulink['customized'] = y.customized
            menulink['p1'] = y.p1
            menulink['p2'] = y.p2
            menulink['p3'] = y.p3
            menulink['p4'] = y.p4
            menulink['p5'] = y.p5
            menulink['p6'] = y.p6
            menulink['p7'] = y.p7
            menulink['p8'] = y.p8
            menulink['p9'] = y.p9
            menulink['updated'] = y.updated
            menu['links'].append(menulink)


        menus.append(menu)
    output['menus'] = menus

    # Redirects

    internalredirects = []
    externalredirects = []
    redirects_result = conn.execute(sqlalchemy.text("select rid, source, redirect, status from redirect;"))
    for x in redirects_result:
        if x.status == 0:
            continue
        redirect = {}

        # redirectfilter = re.compile('node/\d*')


        redirect['rid'] = x.rid
        redirect['source'] = x.source
        redirect['redirect'] = x.redirect

        if redirect['source'][0:5] == 'node/':
            redirect['source'] = urlaliasmap[redirect['source']]

        if redirect['redirect'][0:5] == 'node/':
            redirect['redirect'] = urlaliasmap[redirect['redirect']]


        if x.redirect[0:4] != 'http':
            redirect['redirect'] = 'internal:/' + redirect['redirect']
            internalredirects.append(redirect)
        else:
            externalredirects.append(redirect)

    output['internalredirects'] = internalredirects
    output['externalredirects'] = externalredirects

    # Vocabularies

    vocabularies = {}

    vocabularies_mapping = [
        {'src': 'byline', 'dst': 'byline'},
        {'src': 'department', 'dst': 'department'},
        {'src': 'newsletter', 'dst': 'newsletter'},
        {'src': 'job_type', 'dst': 'ucb_person_job_type'},
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
            term_result = conn.execute(sqlalchemy.text(f"select tid, name, description, format, weight from taxonomy_term_data WHERE vid = '{vid.vid}';"))
            for t in term_result:
                terms.append({'tid': t.tid, 'name': t.name, 'description': t.description, 'format': t.format, 'weight': t.weight})
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


