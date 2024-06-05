from jinja2 import Environment, PackageLoader, select_autoescape
import rich
import yaml
from lxml import etree
from rich import print
import typer

app = typer.Typer()

parent_map = ''
root = ''





def getbean(bid, root, parent_map):
    # print(s.text)
    beans = root.findall(f"./beans//bid")

    for b in beans:
        if b.text == bid:
            return(parent_map[b])

def printbeaninfo(bid, depth, root, parent_map):
    bean = getbean(bid, root, parent_map)
    if bean is None:
        print(f"  BEAN NOT FOUND - {bid}")
        return
    type = bean.find('type').text
    print("  " * depth + f"Bean {bean.find('bid').text} - {type}")

    if type == 'block_section':
        section_blocks = bean.findall('./fields/field_blocks_section_blocks/data/item/field_blocks_section_blocks_target_id')
        for secblocks in section_blocks:
            printbeaninfo(secblocks.text, depth+1, root, parent_map)

    if type == 'block_row':
        row_blocks = bean.findall('./fields/field_block_row_collection/data/item/collection/field_block_row_block/field_block_row_block_target_id')
        for rowblocks in row_blocks:
            printbeaninfo(rowblocks.text, depth+1, root, parent_map)

    # if type == 'feature_callout':
    #     pass
    #     # etree.dump(bean)
    #
    # if type == 'content_sequence':
    #     # etree.dump(bean)
    #     pass
    #
    # if type == 'block':
    #     #etree.dump(bean)
    #     pass
    #
    # if type == 'block_wrapper':
    #     #etree.dump(bean)
    #     pass


def printnodesinfo(nodes, root, parent_map, type):
    for n in nodes:
        # print(f"---")

        # print(f"Layout beans:")
        layouts = n.findall("./layout/fields/item")

        if len(layouts) > 0 and type != 'page':


            if n.find('path') is not None:
                print(f"Node {n.find('nid').text} - {n.find('type').text} - {n.find('title').text} - {n.find('path').text}")
            else:
                print(f"Node {n.find('nid').text} - {n.find('type').text} - {n.find('title').text} - NOPATH")

            for l in layouts:
                # etree.dump(l)
                print(f"Layout: {l.find('name').text}")
                for b in l.findall('./beans/item'):
                    # etree.dump(b)
                    # print(b.text)
                    printbeaninfo(b.text, 1, root, parent_map)
                    pass
                # bid = s.text
                # bean = getbean(bid)
                # etree.dump(bean)

                # printbeaninfo(bid, 0)

@app.command()
def generate_report(name: str):
    print(f'Report for site: {name}')

    siteinfo = {}



    with open(f'sites/{name}/data.xml', "rb") as input:

        root = etree.parse(input).getroot()
        parent_map = {c: p for p in root.iter() for c in p}

        file_node_count = 0
        total_node_count = 0

        print("Node types:")
        node_types = root.findall('./nodes/item')
        for type_root in node_types:
            for type in type_root:
                print(f'---')
                print(f'Type: {type.tag}, Count: {len(type)}')

                total_node_count += len(type)

                if type.tag == 'file':
                    file_node_count = len(type)

                type_root = root.findall(f'./nodes/item/{type.tag}/item')
                printnodesinfo(type_root, root, parent_map, type.tag)

        print('-----')



        file_images = len(root.findall('./files/images/item'))
        file_documents = len(root.findall('./files/documents/item'))


        # print(f'Total Node Count: {total_node_count}')
        # print(f'File Node Count: {file_node_count}')
        #
        # print(f'Image Files: {file_images}')
        # print(f'Document Files: {file_documents}')


        siteinfo['general'] = {}
        siteinfo['general']['sitename'] = name
        siteinfo['general']['file_images'] = len(root.findall('./files/images/item'))
        siteinfo['general']['file_documents'] = len(root.findall('./files/documents/item'))
        siteinfo['general']['file_nodes'] = file_node_count
        siteinfo['general']['total_nodes'] = total_node_count



        print('-----')

        siteinfo['users'] = []


        users = root.findall('./users/item')
        for user in users:
            roles = user.find('roles')
            if roles is not None and len(roles) > 0:
                u = {}
                u['name'] = user.find('name').text
                u['roles'] = []

                # print(user.find('name').text)
                for role in roles:
                    r = {}
                    r['name'] = role.text
                    u['roles'].append(r)
                    # print(f'  {role.text}')
                siteinfo['users'].append(u)
        print('-----')

        siteinfo['taxonomies'] = []

        vocabularies_root = root.findall('./vocabularies')
        for vocabularies in vocabularies_root:
            for vocabulary in vocabularies:
                if len(vocabulary) > 0:
                    v = {}
                    v['tag'] = vocabulary.tag
                    v['terms'] = []
                    # print(f'{vocabulary.tag} - {len(vocabulary)}')
                    terms = vocabulary.findall('item')
                    for term in terms:
                        t = {}
                        t['name'] = term.find("name").text
                        v['terms'].append(t)
                        # print(f'  {term.find("name").text}')
                        pass
                    siteinfo['taxonomies'].append(v)

        print('-----')

        siteinfo['context'] = []

        context_root = root.findall('./context')
        for contexts in context_root:
            for context in contexts:
                c = {}
                c['name'] = context.find('name').text
                c['description'] = context.find('description').text
                siteinfo['context'].append(c)
                # print(f"{context.find('name').text} - {context.find('description').text}")

    env = Environment(
        loader=PackageLoader("report"),
        autoescape=select_autoescape()
    )

    template = env.get_template("report.html")

    print(template.render(info=siteinfo))








if __name__ == "__main__":
    app()