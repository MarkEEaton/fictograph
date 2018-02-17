from pprint import pprint

def clean(data):
    cleaned = []
    for i in range(len(data)):
        try:
            if data[i]['date'] != data[i+1]['date']:
                cleaned.append(data[i])
        except IndexError:
            cleaned.append(data[i])
    pprint(cleaned)
    return cleaned
