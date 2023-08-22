from io import StringIO, BytesIO
import argparse
import re




parser = argparse.ArgumentParser()

parser.add_argument("--input", help="Input database file")

args = parser.parse_args()

print(args)

matches = {}
icon_matches = {}

with open(args.input, "rb") as input:
    s = str(input.read())
    pattern = '\[\/.*?\]'
    icon_pattern = '\[icon.*?\]'
    result = re.findall(pattern, s)

    # for x in result:
    #
    #     #Non-icon shortcodes
    #     y = str(x[2:-1].split()[0])
    #
    #     match = re.findall(r'[\dA-Za-z]*', y)[0]
    #
    #     if match in matches:
    #         matches[match] += 1
    #     else:
    #         matches[match] = 1
    #
    #
    #     #Icon types

    icon_result = re.findall(icon_pattern, s)
    for icon in icon_result:
        #icon_type = icon.split()[1][9:]
        icon_type = icon.split()
        if len(icon_type) < 2:
            print(icon_type)
            continue
        else:
            icon_type = icon_type[1][9:]
        #print(icon_type)

        icon_type = icon_type.split('\\')[0]

        if icon_type in icon_matches:
            icon_matches[icon_type] += 1
        else:
            icon_matches[icon_type] = 1



    #print(matches)

    #print(icon_matches)

    sorted_icons = dict(sorted(icon_matches.items(), key=lambda item: item[1], reverse=True))

    #print(sorted_icons)

    for icon in sorted_icons:
        print(f'{icon}: {sorted_icons[icon]}')

