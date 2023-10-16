"""helper function"""


from collections import namedtuple


# names tuple and variables, example:
# [Box(id=1, name='b2', height=2.0, width=2.0, length=2.0)]
Box = namedtuple("Box", "id name height width length")

Container = namedtuple("Container", "id occupied_volume")

Freight = namedtuple("Freight", "id container_id box_id")