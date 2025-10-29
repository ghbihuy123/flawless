# 2) Tải dữ liệu
wget -O tt100k_2021.zip https://cg.cs.tsinghua.edu.cn/traffic-sign/tt100k_2021.zip
# wget -O nosign_1.zip  https://cg.cs.tsinghua.edu.cn/traffic-sign/data_model_code/nosign_1.zip

# 3) Giải nén
unzip -q tt100k_2021.zip -d ./TT100K
# unzip -q nosign_1.zip  -d ./NoSign

# 4) Chuẩn bị dữ liệu: move ảnh + annotation tới cấu trúc YOLOv8
# Ví dụ:
mkdir -p ./dataset/train/images
mkdir -p ./dataset/train/labels
mkdir -p ./dataset/val/images
mkdir -p ./dataset/val/labels
mkdir -p ./dataset/test/images
mkdir -p ./dataset/test/labels

mv ./TT100K/tt100k_2021/test/* ./dataset/test/images
mv ./TT100K/tt100k_2021/train/* ./dataset/train/images
mv ./TT100K/tt100k_2021/other/* ./dataset/val/images