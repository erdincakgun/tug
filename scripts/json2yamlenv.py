import json
import sys
import os

if len(sys.argv) != 2:
    print("Usage: python3 json2yamlenv.py <json_file_or_folder>")
    sys.exit(1)

input_path = sys.argv[1]

def get_json_paths(data, prefix=''):
    paths = []
    if isinstance(data, dict):
        for key, value in data.items():
            new_prefix = f"{prefix}__{key}" if prefix else key
            if isinstance(value, (dict, list)):
                paths.extend(get_json_paths(value, new_prefix))
            else:
                paths.append((new_prefix, value))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_prefix = f"{prefix}__{i}"
            if isinstance(item, (dict, list)):
                paths.extend(get_json_paths(item, new_prefix))
            else:
                paths.append((new_prefix, item))
    return paths

def process_json_file(json_file, output_dir):
    output_file = os.path.join(output_dir, os.path.basename(json_file))
    output_file = os.path.splitext(output_file)[0] + '.yaml'
    
    with open(json_file, "r") as file:
        data = json.load(file)
    
    paths = get_json_paths(data)
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        for path, value in paths:
            f.write(f"{path}: \"{value}\"\n")

if os.path.isfile(input_path):
    if input_path.endswith('.json'):
        os.makedirs('json2yamlenv', exist_ok=True)
        process_json_file(input_path, 'json2yamlenv')
elif os.path.isdir(input_path):
    for root, _, files in os.walk(input_path):
        for file in files:
            if file.endswith('.json'):
                json_file = os.path.join(root, file)
                rel_path = os.path.relpath(root, input_path)
                output_dir = os.path.join('json2yamlenv', rel_path)
                process_json_file(json_file, output_dir)
else:
    print(f"Error: {input_path} is not a valid file or directory")
    sys.exit(1)
