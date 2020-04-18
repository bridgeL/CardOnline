from collections import defaultdict

site = defaultdict(list)

site[0].append('sdf')
site[1].append(1)
site[4].append(1)

print(site.__len__())
