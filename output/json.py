import ujson


def to_json(results, path):

    output = {x['path']: [] for x in results}
    for x in results:
        output[x['path']].append(x)

    with open(path, 'w') as file:
        ujson.dump(output, file, indent=4)
