import yaml
import rich

sitelist = {}
sitelist['sites'] = []


with open('sitelists/cohort-2-final.yml') as input:
    sitelist1 = yaml.safe_load(input)

with open('sitelists/cohort-2-tolaunch.yml') as input:
    sitelist2 = yaml.safe_load(input)

dst1 = []
dst2 = []

for site in sitelist1['sites']:
    dst1.append(site['dst'])

for site in sitelist2['sites']:
    dst2.append(site['dst'])

# print(dst1)
# print(dst2)

dst3 = [value for value in dst1 if value in dst2]

only1 = [value for value in dst1 if value not in dst2]
print(only1)



