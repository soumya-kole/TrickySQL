def get_kv(k):
    return f"Value of {k} from kv"

from collections import UserDict

class ConfigDict(UserDict):
    def __init__(self, initial_dict=None):
        initial_dict = initial_dict or {}
        super().__init__(initial_dict)
        self.kv_manager = None

    def __getitem__(self, key):
        try:
            if not self.kv_manager:
                self.kv_manager = get_kv
            if self.data[key].startswith('kvval.'):
                return self.kv_manager(self.data[key].split('.')[1].strip())
            else:
                self.data[key]
        except KeyError:
            raise KeyError(key)

import yaml

# Function to read YAML file
def read_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        for k,v in data.items():
            if str(v).startswith('ref'):
                ref = data[k].split(':')[1].strip()
                if len(ref.split('.'))==2:
                    ref_file =ref
                    data[k]=read_yaml(ref_file)
                else:
                    ref_file = f"{ref.split('.')[0]}.{ref.split('.')[1]}"
                    d=read_yaml(ref_file)
                    i = 2
                    while i < len(ref.split('.')):
                        d = d[ref.split('.')[i]]
                        i += 1
                    data[k]=d
    return ConfigDict(data)

# Usage
file_path = 'example.yaml'
data = read_yaml(file_path)
print(type(data))
print(data)
print(data['age'])
