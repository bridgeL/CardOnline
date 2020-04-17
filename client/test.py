from collections import defaultdict

site = defaultdict(list)

site[4].append(1)
site[0].append('sdf')
site[1].append(1)


print(site.__len__())

site_order_list = []

for k in site.keys():
    site_order_list.append(k)

site_order_list.sort()

print(site_order_list)
