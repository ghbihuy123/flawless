from PIL import Image
import os

def convert_to_yolo(xmin, ymin, xmax, ymax, width, height):
    """
    Convert bounding box from absolute coordinates to YOLO format.
    
    Args:
        xmin, ymin, xmax, ymax (float): bounding box coordinates in pixels
        width, height (int): image dimensions in pixels
        
    Returns:
        tuple: (x_center, y_center, w, h) normalized in range [0,1]
    """
    x_center = ((xmin + xmax) / 2) / width
    y_center = ((ymin + ymax) / 2) / height
    w = (xmax - xmin) / width
    h = (ymax - ymin) / height
    return x_center, y_center, w, h

def raw_into_yolo_format_adapter(
    image_id: str,
    image_path: str,
    images_dict: dict,
    classes_list: list,
    output_dir: str
):
    img = Image.open(f"{image_path}/{image_id}.jpg")
    width, height = img.size
    objects = images_dict[image_id]["objects"]

    lines = []
    for object in objects:
        category = object["category"]
        bbox = object["bbox"]
        xmin = bbox["xmin"]
        ymin = bbox["ymin"]
        xmax = bbox["xmax"]
        ymax = bbox["ymax"]
        x_center, y_center, w, h = convert_to_yolo(
            xmin=xmin,
            xmax=xmax,
            ymax=ymax,
            ymin=ymin,
            width=width,
            height=height
        )
        idx = classes_list.index(category)
        lines.append(f"{idx} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}")

    # ---- Ghi ra file .txt ----
    label_path = os.path.join(output_dir, f"{image_id}.txt")
    with open(label_path, "w") as f:
        f.write("\n".join(lines))

    print(f"✅ Saved: {label_path}")