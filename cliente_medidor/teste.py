import json,time

json_string = {"id": 2, "id_medidor": 2,"valor":2.3,"timestamp":time.time()}
json_string = json.dumps(json_string,separators=(',',':'),indent='\t')
print(repr(json_string))