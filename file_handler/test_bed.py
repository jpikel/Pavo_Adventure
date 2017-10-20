import json
from collections import OrderedDict

#reference https://stackoverflow.com/questions/20656135/python-deep-merge-dictionary-data

def merge(source, destination):
    for key, value in source.items():
        if isinstance(value, dict) and not bool(source[key]) and key in destination:
            destination.pop(key, None)
        elif isinstance(value, dict):
            node = destination.setdefault(key,  {})
            merge(value, node)
        else:
            destination[key] = value
    return destination

def gather_dicts(source, key):
    if key in source:
        return source[key]

def add_key_before_dicts(source, key, top_key):
    new_dict = OrderedDict()
    for obj in source:
        new_dict.update({top_key:{obj[key]:obj}})
    return new_dict

def get_order(source):
    order = source.items()
    order_list = []
    for key in order:
        order_list.append(key[0])
    return order_list

a = OrderedDict()
a.update({'title':'title of a'})
a.update({'thisbool':False})
a.update({'long_description':'long in a for deleteion!'})
a.update({'features' : 
            { '1' : { 
                'verbs' :{
                    'use': {
                        'description':'use in a'
                        },
                    'take':{
                        'description':'take in a'
                        }
                    }
                }
            }
    })
a.update({    "connected_rooms": [
        {
            "accessible": True, 
            "distance_from_room": 1, 
            "title": "crash site", 
            "pre_item_description": "", 
            "item_required_title": "", 
            "compass_direction": "", 
            "id": 0, 
            "item_required": False, 
            "aliases": [
                "crash site"
            ]
        }
    ]})


source_order = get_order(a)
b = OrderedDict()
b.update({ 
    'updates':{
        'thisbool':True,
        'connected_rooms':{},
        'long_description':"stuff in b",
        'features' : 
            { '1' : { 
                'verbs' :{
                    'use': {},
                    'take': {
                        'description':''
                        }
                    }
                }
            }
        }
    })

print json.dumps(a, indent=4)
print json.dumps(b, indent=4)
#get the old connected_rooms
old_dict = gather_dicts(a, 'connected_rooms')
print json.dumps(old_dict, indent=4)
c = OrderedDict()
#delete the connected rooms
c = merge(b['updates'], a)
#new_dict = add_key_before_dicts(old_dict, 'title', 'connected_rooms')
#d = merge(new_dict, c)
#z = OrderedDict(sorted(c.items(), key=lambda i:source_order.index(i[0])))
print json.dumps(c, indent=4)
