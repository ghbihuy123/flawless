import requests
import json

API_URL = "https://api-inference.huggingface.co/models/LanguageBind/Video-LLaVA-7B"
headers = {"Authorization": "Bearer hf"}  # <-- HF token

def query(video_path, question, choices):
    prompt = f"Câu hỏi: {question}\nCác lựa chọn:\n" + "\n".join(choices)

    with open("./traffic_buddy_train+public_test/traffic_buddy_train+public_test/" + video_path, "rb") as f:
        files = {"file": f}
        payload = {"inputs": prompt}

        response = requests.post(API_URL, headers=headers, data=payload, files=files)

    print("Status code:", response.status_code)
    print("Response text:", response.text[:500])  # debug xem server trả gì

    try:
        return response.json()
    except Exception:
        return {"error": response.text}

data = json.load(open("./traffic_buddy_train+public_test/traffic_buddy_train+public_test/train/train.json"))
item = data["data"][0]
print(query(item["video_path"], item["question"], item["choices"]))
