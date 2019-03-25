import json
import pprint

with open('match_records/2019_02_02_08_00', 'r') as f:
    data = f.read()
    print(data)
    json_data = json.loads(data)
    print(json_data)

    
    pprint.pprint(json_data)