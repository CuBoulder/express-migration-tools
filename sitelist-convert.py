import yaml
import rich

sitelist = {}
sitelist['sites'] = []


with open('autositelistcomplete.txt') as input:
    for line in input:
        line = line.strip()
        if len(line) == 0:
            continue
        line = line.split(',')
        site = {}
        site['src'] = line[0]
        site['path'] = line[1]
        site['dst'] = 'ucbprod-' + line[0][4:]
        # rich.print(site)
        found = False
        for s in sitelist['sites']:
            if s['src'] == site['src']:
                found = True
        if found != True:
            sitelist['sites'].append(site)

# rich.print(sitelist)
print(yaml.dump(sitelist))
