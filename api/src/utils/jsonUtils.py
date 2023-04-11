import json


def objectArrayToJson(objectArray):
    objects = []
    for object in objectArray:
        objects.append(object.__dict__)

    return (json.dumps(objects))
