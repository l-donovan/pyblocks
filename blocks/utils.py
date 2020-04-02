def listify(item):
    return [item] if (type(item) not in [tuple, list]) else item
