import json

data_path = "./TT100K/tt100k_2021"

with open(f"{data_path}/annotations_all.json") as f:
    annotations = json.load(f)

print(annotations["types"])
print(len(annotations["types"]))
