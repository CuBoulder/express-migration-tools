from io import StringIO, BytesIO
import argparse
import re



parser = argparse.ArgumentParser()

parser.add_argument("--input", help="Input database file")

args = parser.parse_args()

print(args)

matches = {}

with open(args.input, "rb") as input:
    s = str(input.read())
    pattern = '\[\/.*?\]'
    pattern = '\[icon'
    result = re.findall(pattern, s)

    for x in result:
        print(x)
        if x in matches:
            matches[x] += 1
        else:
            matches[x] = 0

    print(matches)

