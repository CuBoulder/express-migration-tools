import yaml
import rich

sitelist = {}
sitelist['sites'] = []


with open('sitelists/cohort-2.yml', 'r') as input:

    y = yaml.safe_load(input)

    for key in y['sites']:
        # print(key)

        print(f"{key['src']},/{key['path']},{key['dst']},{key['training']},https://live-{key['dst']}.pantheonsite.io,https://live-{key['training']}.pantheonsite.io")



# rich.print(sitelist)
# print(yaml.dump(sitelist))
