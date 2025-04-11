import json
data = {'Sword' : [0, 0, 0, 0],
       'Stileto':[0, 0, 0, 1]}

def save(data, file_to_save_in = 'weapon_stats.json'):
    saveFile = open(file_to_save_in, 'w')
    saveFile.write(json.dumps(data, indent = 4))
    saveFile.close()

def load(file_to_load_from = 'weapon_stats.json'):
    saveFile = open(file_to_load_from, 'r')
    data = json.load(saveFile)
    saveFile.close()
    return data

data = load()
save(data)
print(data)