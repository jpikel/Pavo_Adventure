import json
from collections import OrderedDict

#reference https://stackoverflow.com/questions/20656135/python-deep-merge-dictionary-data

def merge(source, destination):
    for key, value in source.items():
        if isinstance(value, dict):
            node = destination.setdefault(key,  {})
            merge(value, node)
        else:
            destination[key] = value
    return destination

def get_order(source):
    order = source.items()
    order_list = []
    for key in order:
        order_list.append(key[0])
    return order_list

a = OrderedDict()
a.update({'title':'title of a'})
a.update({'long_description':'long in a'})
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

source_order = get_order(a)
b = OrderedDict()
b.update({ 
    'updates':{
        'long_description':'new long',
        'features' : 
            { '1' : { 
                'verbs' :{
                    'use': {
                        'description':'use in b'
                        }
                    }
                }
            }
        }
    })

#print json.dumps(a, indent=4)
#print json.dumps(b, indent=4)
c = OrderedDict()
c = merge(b['updates'], a)
z = OrderedDict(sorted(c.items(), key=lambda i:source_order.index(i[0])))
print json.dumps(z, indent=4)
