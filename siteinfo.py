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
            bean = getbean(bid)
            # etree.dump(bean)


            print(f"Bean {bean.find('bid').text} - {bean.find('type').text}")

            section_blocks = bean.findall('./fields/field_blocks_section_blocks/data/item/field_blocks_section_blocks_target_id')
            for secblocks in section_blocks:
                secbean = getbean(secblocks.text)
                print(f"  Bean {secbean.find('bid').text} - {secbean.find('type').text}")



