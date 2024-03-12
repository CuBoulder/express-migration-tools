from lxml import etree
from io import StringIO, BytesIO
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--input", help="Input XML file")
parser.add_argument("--beans", help="Only show nodes with beans")

args = parser.parse_args()

print(args)

parent_map = ''
root = ''


def getbean(bid):
    # print(s.text)
    beans = root.findall(f"./beans//bid")

    for b in beans:
        if b.text == bid:
            return(parent_map[b])

def printbeaninfo(bid, depth):
    bean = getbean(bid)
    if bean is None:
        print(f"  BEAN NOT FOUND - {bid}")
        return
    type = bean.find('type').text
    print("  " * depth + f"Bean {bean.find('bid').text} - {type}")

    if type == 'block_section':
        section_blocks = bean.findall('./fields/field_blocks_section_blocks/data/item/field_blocks_section_blocks_target_id')
        for secblocks in section_blocks:
            printbeaninfo(secblocks.text, depth+1)

    if type == 'block_row':
        row_blocks = bean.findall('./fields/field_block_row_collection/data/item/collection/field_block_row_block/field_block_row_block_target_id')
        for rowblocks in row_blocks:
            printbeaninfo(rowblocks.text, depth+1)

    if type == 'feature_callout':
        pass
        # etree.dump(bean)

    if type == 'content_sequence':
        # etree.dump(bean)
        pass

    if type == 'block':
        #etree.dump(bean)
        pass

    if type == 'block_wrapper':
        #etree.dump(bean)
        pass


def printnodesinfo(nodes):
    for n in nodes:
        print(f"---")
        if n.find('path') is not None:
            print(f"Node {n.find('nid').text} - {n.find('type').text} - {n.find('title').text} - {n.find('path').text}")
        else:
            print(f"Node {n.find('nid').text} - {n.find('type').text} - {n.find('title').text} - NOPATH")
        # print(f"Layout beans:")
        layouts = n.findall("./layout/fields/item")
        for l in layouts:
            # etree.dump(l)
            print(f"Layout: {l.find('name').text}")
            for b in l.findall('./beans/item'):
                # etree.dump(b)
                # print(b.text)
                printbeaninfo(b.text, 1)
            # bid = s.text
            # bean = getbean(bid)
            # etree.dump(bean)

            # printbeaninfo(bid, 0)


with open(args.input, "rb") as input:
    root = etree.parse(input).getroot()
    parent_map = {c: p for p in root.iter() for c in p}

    pages = root.findall('./nodes/item/page/item')
    articles = root.findall('./nodes/item/article/item')
    article_list_pages = root.findall('./nodes/item/article_list_page/item')
    people_list_pages = root.findall('./nodes/item/people_list_page/item')
    persons = root.findall('./nodes/item/person/item')
    webforms = root.findall('./nodes/item/webform/item')
    section_pages = root.findall('./nodes/item/section_page/item')
    newsletters = root.findall('./nodes/item/newsletter/item')
    photo_galleries = root.findall('./nodes/item/photo_gallery/item')

    printnodesinfo(pages)
    printnodesinfo(articles)
    printnodesinfo(article_list_pages)
    printnodesinfo(people_list_pages)
    printnodesinfo(persons)
    printnodesinfo(webforms)
    printnodesinfo(newsletters)
    printnodesinfo(photo_galleries)

    # for n in pages:
    #     print(f"---")
    #     print(f"Node {n.find('nid').text} - {n.find('type').text} - {n.find('title').text} - {n.find('path').text}")
    #     #print(f"Layout beans:")
    #     layouts = n.findall("./layout/fields/item")
    #     for l in layouts:
    #         #etree.dump(l)
    #         print(f"Layout: {l.find('name').text}")
    #         for b in l.findall('./beans/item'):
    #             #etree.dump(b)
    #             #print(b.text)
    #             printbeaninfo(b.text, 1)
    #         #bid = s.text
    #         # bean = getbean(bid)
    #         # etree.dump(bean)
    #
    #         #printbeaninfo(bid, 0)

    sectionpages = root.findall('./nodes/item/section_page/item')

    for n in sectionpages:
        # etree.dump(n)
        print(f"---")
        print(f"Node {n.find('nid').text} - {n.find('type').text} - {n.find('title').text} - {n.find('path').text}")
        print(f"Page sections:")
        sections = n.findall(".//field_section_page_sections/data/item/field_section_page_sections_target_id")
        for s in sections:
            bid = s.text
            # bean = getbean(bid)
            # etree.dump(bean)

            printbeaninfo(bid, 1)






