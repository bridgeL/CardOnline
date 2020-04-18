from collections import defaultdict

site = defaultdict(list)

<<<<<<< HEAD
site[0].append('sdf')
site[1].append(1)
site[4].append(1)

print(site.__len__())
=======
site[4].append(1)
site[0].append('sdf')
site[1].append(1)


print(site.__len__())

site_order_list = []

for k in site.keys():
    site_order_list.append(k)

site_order_list.sort()

print(site_order_list)
>>>>>>> parent of c875951... gameroom mode improve
