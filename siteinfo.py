from lxml import etree
from io import StringIO, BytesIO
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--input", help="Input XML file")

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
    type = bean.find('type').text
    print("  " * depth + f"Bean {bean.find('bid').text} - {type}")

    if type == 'block_section':
        section_blocks = bean.findall('./fields/field_blocks_section_blocks/data/item/field_blocks_section_blocks_target_id')
        for secblocks in section_blocks:
            printbeaninfo(secblocks.text, depth+1)

    if type == 'feature_callout':
        pass
        # etree.dump(bean)

    if type == 'content_sequence':
        etree.dump(bean)





with open(args.input, "rb") as input:
    root = etree.parse(input).getroot()
    parent_map = {c: p for p in root.iter() for c in p}


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

            printbeaninfo(bid, 0)






