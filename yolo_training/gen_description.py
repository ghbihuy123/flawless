names = [
"pl80","w9","p6","ph4.2","i8","w14","w33","pa13","im","w58","pl90","il70","p5","pm55","pl60","ip","p11","pdd","wc","i2r","w30","pmr","p23","pl15","pm10","pss","w1","p4","w38","w50","w34","pw3.5","iz","w39","w11","p1n","pr70","pd","pnl","pg","ph5.3","w66","il80","pb","pbm","pm5","w24","w67","w49","pm40","ph4","w45","i4","w37","ph2.6","pl70","ph5.5","i14","i11","p7","p29","pne","pr60","pm13","ph4.5","p12","p3","w40","pl5","w13","pr10","p14","i4l","pr30","pw4.2","w16","p17","ph3","i9","w15","w35","pa8","pt","pr45","w17","pl30","pcs","pctl","pr50","ph4.4","pm46","pm35","i15","pa12","pclr","i1","pcd","pbp","pcr","w28","ps","pm8","w18","w2","w52","ph2.9","ph1.8","pe","p20","w36","p10","pn","pa14","w54","ph3.2","p2","ph2.5","w62","w55","pw3","pw4.5","i12","ph4.3","phclr","i10","pr5","i13","w10","p26","w26","p8","w5","w42","il50","p13","pr40","p25","w41","pl20","ph4.8","pnlc","ph3.3","w29","ph2.1","w53","pm30","p24","p21","pl40","w27","pmb","pc","i6","pr20","p18","ph3.8","pm50","pm25","i2","w22","w47","w56","pl120","ph2.8","i7","w12","pm1.5","pm2.5","w32","pm15","ph5","w19","pw3.2","pw2.5","pl10","il60","w57","w48","w60","pl100","pr80","p16","pl110","w59","w64","w20","ph2","p9","il100","w31","w65","ph2.4","pr100","p19","ph3.5","pa10","pcl","pl35","p15","w7","pa6","phcs","w43","p28","w6","w3","w25","pl25","il110","p1","w46","pn-2","w51","w44","w63","w23","pm20","w8","pmblr","w4","i5","il90","w21","p27","pl50","pl65","w61","ph2.2","pm2","i3","pa18","pw4"
]

import re, json, math

def gen_description(code):
    # General category based on prefix
    desc_vi = ""
    desc_en = ""
    note = ""
    if re.match(r'^w', code):
        # warning
        desc_vi = f"Biển cảnh báo (ký hiệu {code}): cảnh báo nguy hiểm trên đường phía trước; xe cơ giới cần chú ý, giảm tốc và quan sát."
        desc_en = f"Warning sign (code {code}): warns of a hazard ahead; drivers should be cautious, slow down and observe."
    elif re.match(r'^p', code):
        # prohibitory or regulatory
        desc_vi = f"Biển cấm/hạn chế (ký hiệu {code}): báo hiệu cấm hoặc hạn chế hành vi giao thông cụ thể; người tham gia giao thông phải tuân thủ."
        desc_en = f"Prohibitory/regulatory sign (code {code}): indicates a prohibition or restriction; road users must comply."
    elif re.match(r'^i', code):
        # informative / instruction / mandatory
        desc_vi = f"Biển chỉ dẫn/khuyến cáo (ký hiệu {code}): hướng dẫn hoặc bắt buộc người tham gia giao thông đi theo chỉ dẫn."
        desc_en = f"Instruction/mandatory sign (code {code}): provides direction or mandatory instructions for road users."
    else:
        desc_vi = f"Biển giao thông (ký hiệu {code}): mô tả tổng quát dựa trên ký hiệu."
        desc_en = f"Traffic sign (code {code}): general description inferred from code."
    
    # specific pattern extra details (inferred from common suffixes)
    # height limit phX -> chiều cao (m)
    m = re.match(r'^ph([0-9]+(?:\.[0-9]+)?)$', code)
    if m:
        h = m.group(1)
        desc_vi = f"Biển hạn chế chiều cao: cấm những phương tiện có chiều cao vượt quá {h} mét đi qua. Lái xe cần chú ý chiều cao hàng hóa và tải."
        desc_en = f"Height restriction sign: prohibits vehicles taller than {h} m from passing. Drivers must check vehicle/load height."
        note = "inferred: 'ph' interpreted as height (m)."
    # weight limit pmX -> khối lượng/tải trọng (tấn)
    m = re.match(r'^pm([0-9]+(?:\.[0-9]+)?)$', code)
    if m:
        w = m.group(1)
        desc_vi = f"Biển hạn chế trọng tải: cấm xe có khối lượng toàn phần trên {w} tấn đi qua (áp dụng cho trục hoặc tổng tải tuỳ biển)."
        desc_en = f"Weight limit sign: prohibits vehicles with gross weight over {w} tonnes from passing (may apply to axle or total weight depending on sign)."
        note = "inferred: 'pm' interpreted as permissible mass/weight (tấn)."
    # width limit pwX -> bề rộng (m)
    m = re.match(r'^pw([0-9]+(?:\.[0-9]+)?)$', code)
    if m:
        wid = m.group(1)
        desc_vi = f"Biển hạn chế bề rộng: cấm những phương tiện có bề rộng lớn hơn {wid} mét đi qua."
        desc_en = f"Width restriction sign: prohibits vehicles wider than {wid} m from passing."
        note = "inferred: 'pw' interpreted as width (m)."
    # speed/limit-like plNN -> inferred as numeric limit (could be speed or length) - image shows pl## many values
    m = re.match(r'^pl([0-9]+)$', code)
    if m:
        val = m.group(1)
        desc_vi = f"Biển hạn chế giới hạn (ký hiệu {code}): giá trị {val} được thể hiện trên biển (inferred: có thể là giới hạn tốc độ hoặc giới hạn khác theo ngữ cảnh)."
        desc_en = f"Limit sign (code {code}): value {val} displayed on sign (inferred: may indicate speed or other numeric limit depending on context)."
        note = "inferred: 'pl' is numeric-labeled limit; confirm exact meaning from reference."
    # prNN -> 'pr' could be radius/turn or 'r' for 'rẽ' -> but many pr values like pr70 pr100 etc: infer numeric restriction (possibly speed advisory/limit)
    m = re.match(r'^pr([0-9]+)$', code)
    if m:
        val = m.group(1)
        desc_vi = f"Biển chỉ giới hạn/giá trị (ký hiệu {code}): hiển thị giá trị {val} (inferred: có thể là giới hạn tốc độ hoặc chỉ dẫn khác)."
        desc_en = f"Value sign (code {code}): displays value {val} (inferred: possibly a speed or other actionable limit)."
        note = "inferred: 'pr' numeric; verify with standard."
    # pn-2 or pn variants -> parking or no parking pn, pnl, pnlc
    if code.startswith('pn'):
        if code in ('pn','pnl','pnlc','pn-2'):
            desc_vi = f"Biển liên quan đến chỗ đỗ/không đỗ (ký hiệu {code}): chỉ dẫn/ cấm dừng/đỗ theo ký hiệu phụ."
            desc_en = f"Parking/No-parking related sign (code {code}): indicates parking or no-parking rules, possibly with supplementary plates."
            note = "inferred: 'pn' family = parking related."
    # p1, p2 ... specific prohibitory common ones
    if re.match(r'^p[0-9]+$', code):
        num = re.findall(r'\d+', code)[0]
        desc_vi = f"Biển cấm (P{num}): cấm một hành vi giao thông cụ thể (ví dụ: cấm quay đầu, cấm rẽ, cấm xe cơ giới...); xem biểu tượng để biết hành vi bị cấm."
        desc_en = f"Prohibitory sign (P{num}): prohibits a specific traffic action (e.g., no U-turn, no left turn, no motor vehicles); refer to symbol for exact prohibition."
    # i + number + optional letters (i2r, i4l, i4l etc)
    m = re.match(r'^i(\d+)([a-z]*)$', code)
    if m:
        num = m.group(1)
        suf = m.group(2)
        desc_vi = f"Biển chỉ dẫn (I{num}{suf}): chỉ dẫn hướng đi hoặc hành vi bắt buộc; thường là mũi tên hoặc biểu tượng phương tiện."
        desc_en = f"Mandatory/directional sign (I{num}{suf}): instructs a direction or mandatory action; commonly arrows or vehicle icons."
    # other specific short codes commonly used:
    extras = {
        'ip': ("Biển chỉ đường/biển phụ chỉ vị trí trạm kiểm soát/qua cầu", "Guide/indicative sign (position of control/checkpoint or bridge)"),
        'im': ("Biển thông tin bổ sung/biển phụ", "Supplementary/Information plate"),
        'wc': ("Khu vực có WC/nơi nghỉ", "Toilet/rest area (inferred)"),
        'pt': ("Biển liên quan trạm thu phí/paid toll", "Toll station sign (inferred)"),
        'ps': ("Biển 'Stop' hoặc dừng lại (in many standards 'ps' = stop)", "Stop sign (inferred)"),
        'pc': ("Biển cấm/giới hạn (pc): ký hiệu phụ, cần tham chiếu biểu tượng", "Prohibitory/Control sign (inferred)"),
        'pe': ("Biển chỉ dẫn chiều đi hoặc cấm (inferred)", "Direction/entry sign (inferred)"),
        'pcs': ("Biển chỉ dẫn đặc biệt/chi tiết (inferred)", "Special guidance (inferred)"),
        'pctl':("Biển liên quan cấm/giới hạn theo tuyến (inferred)", "Route-based control (inferred)"),
        'pcl':("Biển phụ/biển cảnh báo phụ (inferred)", "Supplementary plate (inferred)"),
        'pclr':("Biển hoặc ký hiệu liên quan màu sắc/chiều (inferred)", "Color/clarification plate (inferred)"),
        'pb':("Biển phụ/biển báo phụ (inferred)","Supplementary sign (inferred)"),
        'pbm':("Biển phụ dạng mũi tên/biển phụ điều chỉnh (inferred)","Supplementary arrow/adjustment plate (inferred)"),
        'pbp':("Biển phụ chỉ giới hạn điểm (inferred)","Point-based supplementary plate (inferred)"),
        'pcr':("Biển điều chỉnh/giới hạn (inferred)","Control/regulatory (inferred)"),
        'pdd':("Biển dừng chờ/đi chậm (inferred)","Stop/wait or slow-down advisory (inferred)"),
        'pcs':("Biển chỉ dẫn đặc biệt (inferred)","Special instruction (inferred)"),
        'pne':("Biển liên quan đến lối vào/ra (inferred)","Entrance/exit related (inferred)"),
        'pmb':("Biển phụ (inferred)","Supplementary sign (inferred)"),
        'pmb':("Biển phụ (inferred)","Supplementary sign (inferred)"),
        'pmblr':("Biển giới hạn khối lượng trục (inferred)","Axle-load limit (inferred)"),
        'pnlc':("Biển liên quan đỗ xe (inferred)","Parking no-left/complex (inferred)"),
        'phclr':("Biển giới hạn chiều cao có ký hiệu màu (inferred)","Colored height restriction (inferred)"),
        'phcs':("Biển giới hạn chiều cao dạng cố định đặc biệt (inferred)","Special height restriction (inferred)"),
    }
    
    if code in extras:
        desc_vi = extras[code][0]
        desc_en = extras[code][1]
        note = "inferred: special-case code."
    
    # produce final object
    obj = {
        "vi": desc_vi,
        "en": desc_en
    }
    if note:
        obj["_note"] = note + " Descriptions inferred from code pattern and provided image; please verify with official standard QCVN 41:2019."
    return obj

mapping = {}
for n in names:
    mapping[n] = gen_description(n)

# save to file
out_path = "./traffic_signs.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(mapping, f, ensure_ascii=False, indent=2)

