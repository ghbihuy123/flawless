import json
import yaml
from utils.gen_labels import raw_into_yolo_format_adapter

data_path = "./TT100K/tt100k_2021"

with open("./dataset.yaml") as f:
    dataset_meta = yaml.safe_load(f)
    classes_list = dataset_meta["names"]

with open(f"{data_path}/annotations_all.json") as f:
    annotations = json.load(f)
    images_dict = annotations["imgs"]

with open("dataset/train/images/ids.txt", "r") as f:
    train_list = [int(line.strip()) for line in f if line.strip()]

with open("dataset/test/images/ids.txt", "r") as f:
    test_list = [int(line.strip()) for line in f if line.strip()]

with open("dataset/val/images/ids.txt", "r") as f:
    val_list = [int(line.strip()) for line in f if line.strip()]

count_train = 0
count_test = 0
count_val = 0
for train_image_id in train_list:
    try:
        raw_into_yolo_format_adapter(
            image_id=str(train_image_id),
            image_path="dataset/train/images",
            images_dict=images_dict,
            classes_list=classes_list,
            output_dir="dataset/train/labels"
        )
        count_train += 1
    except:
        print(f"Not found {train_image_id}")

for test_image_id in test_list:
    try:
        raw_into_yolo_format_adapter(
        image_id=str(test_image_id),
        image_path="dataset/test/images",
        images_dict=images_dict,
        classes_list=classes_list,
        output_dir="dataset/test/labels"
        )
        count_test += 1
    except:
        print(f"Not found {test_image_id}")

for val_image_id in val_list:
    try:
        raw_into_yolo_format_adapter(
        image_id=str(val_image_id),
        image_path="dataset/val/images",
        images_dict=images_dict,
        classes_list=classes_list,
        output_dir="dataset/val/labels"
        )
        count_val += 1
    except:
        print(f"Not found {val_image_id}")

print(f"count train: {count_train}")
print(f"count test: {count_test}")
print(f"count val: {count_val}")