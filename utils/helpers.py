import json

def get_json_structure(obj, indent=0):
    prefix = "  " * indent
    if isinstance(obj, dict):
        for key, value in obj.items():
            #print(f"{prefix}{key}:")
            get_json_structure(value, indent + 1)
    elif isinstance(obj, list):
        #print(f"{prefix}- list[{len(obj)}]")
        if obj:
            get_json_structure(obj[0], indent + 1)
    # else:
    #     #print(f"{prefix}- {type(obj).__name__}")

def write_json_string_to_file(json_string, filename):
    file_path = f"./test_results/{filename}"
    data = json.loads(json_string)  # parse string into dict
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)  # write with formatting

def write_json_to_file(json_obj, filename):
    file_path = f"./test_results/{filename}"
    with open(file_path, "w") as f:
        json.dump(json_obj, f, indent=2) # write with formatting




if __name__ == "__main__":
    json_str = '{"user":{"id":1,"name":"Alice","roles":["admin","user"]},"active":true}'
    data = json.loads(json_str)

    get_json_structure(data)
