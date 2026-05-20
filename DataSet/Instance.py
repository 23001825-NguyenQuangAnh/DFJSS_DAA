"""
Processing_time: Ma trận thời gian gia công của từng công đoạn trên các máy tương ứng
J: Từ điển lưu số lượng công đoạn của từng công việc
M_num: Số lượng máy gia công (Mở rộng lên 20)
O_num: Tổng số công đoạn gia công
J_num: Số lượng công việc (Mở rộng lên 15)
Arrival_Time: Thời điểm các công việc đến xưởng (Sự kiện động)
Breakdowns: Sự kiện máy hỏng đột xuất
Due_Dates: Ngày hạn định hoàn thành cho từng Job
"""

import random

# LOẠI 1: Quy trình gồm 5 công đoạn (Tương thích 20 máy)
CKS_Type1 = [
    [10, 9, 15, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 12, 9999, 9999, 9999, 18, 9999, 9999, 9999, 9999, 9999],
    [9999, 9999, 14, 16, 12, 9999, 9999, 9999, 9999, 9999, 9999, 11, 9999, 9999, 9999, 9999, 15, 9999, 9999, 9999],
    [9999, 9999, 9999, 9999, 15, 25, 21, 9999, 9999, 9999, 9999, 9999, 14, 17, 9999, 9999, 9999, 9999, 9999, 20],
    [9999, 9999, 9999, 9999, 9999, 9999, 9999, 9, 13, 15, 24, 9999, 9999, 9999, 9999, 10, 9999, 12, 9999, 9999],
    [9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 10, 15, 9999, 9999, 9999, 12, 9999, 18, 14]
]

# LOẠI 2: Quy trình gồm 8 công đoạn (Tương thích 20 máy)
CKS_Type2 = [
    [12, 9, 10, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 11, 9999, 9999, 9999, 13, 9999, 9999, 9999, 9999],
    [9999, 9999, 9999, 16, 14, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 15, 9999, 9999, 9999, 9999, 12, 9999, 9999],
    [9999, 9999, 9999, 9999, 15, 18, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 14, 9999, 9999, 9999, 9999, 19, 9999],
    [9999, 9999, 9999, 9999, 9999, 27, 22, 19, 9999, 9999, 9999, 9999, 9999, 9999, 20, 9999, 9999, 9999, 9999, 15],
    [9999, 9999, 9999, 9999, 9999, 9999, 9999, 21, 17, 16, 9999, 9999, 9999, 9999, 9999, 18, 9999, 9999, 9999, 9999],
    [9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 19, 14, 9999, 9999, 9999, 9999, 9999, 15, 9999, 9999, 9999],
    [9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 17, 13, 12, 9999, 9999, 9999, 9999, 11, 9999, 9999],
    [9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 18, 9999, 15, 14, 9999, 9999, 9999, 16, 12]
]

# LOẠI 3: Quy trình phức tạp gồm 10 công đoạn (Tương thích 20 máy)
CKS_Type3 = [
    [8, 12, 9999, 9999, 9999, 15, 9999, 9999, 9999, 9999, 9999, 9999, 10, 9999, 9999, 9999, 14, 9999, 9999, 9999],
    [9999, 9999, 11, 14, 9999, 9999, 9999, 12, 9999, 9999, 9999, 9999, 9999, 15, 9999, 9999, 9999, 18, 9999, 9999],
    [9999, 9999, 9999, 9999, 13, 10, 9999, 9999, 18, 9999, 9999, 9999, 9999, 9999, 12, 9999, 9999, 9999, 16, 9999],
    [9999, 9999, 9999, 9999, 9999, 9999, 16, 15, 9999, 11, 9999, 9999, 9999, 9999, 9999, 14, 9999, 9999, 9999, 13],
    [9999, 15, 9999, 9999, 9999, 9999, 9999, 9999, 14, 12, 17, 9999, 9999, 9999, 9999, 9999, 10, 9999, 9999, 9999],
    [9999, 9999, 10, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 14, 15, 9999, 9999, 9999, 9999, 9999, 11, 14, 9999],
    [9999, 9999, 9999, 12, 16, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 13, 18, 9999, 9999, 9999, 9999, 9999, 15],
    [9999, 9999, 9999, 9999, 9999, 14, 11, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 15, 12, 9999, 9999, 9999, 9999],
    [12, 9999, 9999, 9999, 9999, 9999, 9999, 10, 15, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 14, 9999, 9999, 18],
    [9999, 10, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 14, 11, 9999, 9999, 9999, 16, 9999, 9999, 13, 15, 9999]
]

# ==========================================
# CÁC KỊCH BẢN THỰC NGHIỆM (SCENARIOS)
# ==========================================
# Thay đổi giá trị SCENARIO (1 -> 12) để chạy các bộ dữ liệu khác nhau
SCENARIO = 7

# ==========================================
# NHÓM 1 (KỊCH BẢN 1-6): QUY MÔ NHỎ & TRUNG BÌNH (Dành cho GA / Hybrid)
# ==========================================

if SCENARIO == 1:
    # KỊCH BẢN 1: QUY MÔ NHỎ & TĨNH (BASELINE)
    Processing_time = [CKS_Type1] * 2 + [CKS_Type2] * 2 + [CKS_Type3] * 2
    M_num = 20
    J_num = 6
    J = {i: (5 if i <= 2 else (8 if i <= 4 else 10)) for i in range(1, J_num + 1)}
    O_num = sum(J.values())

    Arrival_Time = [0] * J_num
    Breakdowns = []
    Due_Dates = [100, 110, 150, 160, 200, 210]

elif SCENARIO == 2:
    # KỊCH BẢN 2: QUY MÔ TRUNG BÌNH & ĐỘNG MẠNH (HIGH DYNAMIC)
    Processing_time = [CKS_Type1] * 4 + [CKS_Type2] * 3 + [CKS_Type3] * 3
    M_num = 20
    J_num = 10
    J = {i: (5 if i <= 4 else (8 if i <= 7 else 10)) for i in range(1, J_num + 1)}
    O_num = sum(J.values())

    Arrival_Time = [0, 0, 10, 15, 30, 30, 45, 50, 60, 60]
    Breakdowns = [
        {'machine': 2, 'start': 10, 'duration': 40},
        {'machine': 10, 'start': 35, 'duration': 25},
        {'machine': 11, 'start': 60, 'duration': 30},
        {'machine': 14, 'start': 85, 'duration': 20}
    ]
    Due_Dates = [80, 90, 120, 130, 160, 170, 200, 220, 250, 260]

elif SCENARIO == 3:
    # KỊCH BẢN 3: QUY MÔ LỚN & PHỨC TẠP (BẢN GỐC)
    Processing_time = [CKS_Type1] * 5 + [CKS_Type2] * 5 + [CKS_Type3] * 5
    M_num = 20
    J_num = 15
    J = {i: (5 if i <= 5 else (8 if i <= 10 else 10)) for i in range(1, J_num + 1)}
    O_num = sum(J.values())

    Arrival_Time = [0, 0, 0, 0, 0, 25, 25, 25, 50, 50, 50, 50, 80, 80, 80]
    Breakdowns = [
        {'machine': 1, 'start': 20, 'duration': 30},
        {'machine': 7, 'start': 40, 'duration': 25},
        {'machine': 14, 'start': 60, 'duration': 20},
        {'machine': 4, 'start': 90, 'duration': 15},
        {'machine': 17, 'start': 110, 'duration': 40}
    ]
    Due_Dates = [100, 110, 120, 130, 140, 160, 180, 200, 220, 250, 280, 300, 320, 350, 380]

elif SCENARIO == 4:
    # KỊCH BẢN 4: THẮT NÚT CỔ CHAI (BOTTLENECK)
    J_num = 10
    M_num = 20
    CKS_BOTTLE = []
    for row in CKS_Type2:
        new_row = [p * 3 if i < 2 and p != 9999 else p for i, p in enumerate(row)]
        CKS_BOTTLE.append(new_row)

    Processing_time = [CKS_BOTTLE] * J_num
    J = {i: 8 for i in range(1, J_num + 1)}
    O_num = sum(J.values())

    Arrival_Time = [0] * J_num
    Breakdowns = []
    Due_Dates = [500] * J_num

elif SCENARIO == 5:
    # KỊCH BẢN 5: ĐƠN HÀNG KHẨN CẤP (URGENT ORDERS)
    J_num = 12
    M_num = 20
    Processing_time = [CKS_Type1] * 4 + [CKS_Type2] * 4 + [CKS_Type3] * 4
    J = {i: (5 if i <= 4 else (8 if i <= 8 else 10)) for i in range(1, J_num + 1)}
    O_num = sum(J.values())

    Arrival_Time = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
    Breakdowns = [{'machine': 5, 'start': 50, 'duration': 30}]
    Due_Dates = [60, 70, 80, 100, 110, 120, 140, 150, 170, 190, 210, 230]

elif SCENARIO == 6:
    # KỊCH BẢN 6: XƯỞNG SẢN XUẤT HỖN LOẠN (CHAOS)
    J_num = 8
    M_num = 20
    Processing_time = [CKS_Type2] * 4 + [CKS_Type3] * 4
    J = {i: (8 if i <= 4 else 10) for i in range(1, J_num + 1)}
    O_num = sum(J.values())

    Arrival_Time = [0, 20, 40, 60, 0, 20, 40, 60]
    Breakdowns = [
        {'machine': 0, 'start': 10, 'duration': 20},
        {'machine': 2, 'start': 30, 'duration': 15},
        {'machine': 4, 'start': 50, 'duration': 25},
        {'machine': 8, 'start': 70, 'duration': 20},
        {'machine': 12, 'start': 10, 'duration': 40},
        {'machine': 15, 'start': 90, 'duration': 30},
        {'machine': 18, 'start': 40, 'duration': 20},
        {'machine': 19, 'start': 120, 'duration': 25}
    ]
    Due_Dates = [300] * J_num

# ==========================================
# NHÓM 2 (KỊCH BẢN 7-9): QUY MÔ LỚN (1000 - 1500 Jobs)
# Mục đích: Điểm ngọt để huấn luyện luật GP (Genetic Programming)
# ==========================================

elif SCENARIO == 7:
    # KỊCH BẢN 7: DÒNG CHẢY SẢN XUẤT LIÊN TỤC (STEADY FLOW)
    random.seed(107)
    J_num = 1000
    M_num = 20
    Job_types = random.choices([1, 2, 3], weights=[0.4, 0.4, 0.2], k=J_num)
    Processing_time = []
    J = {}
    for i, t in enumerate(Job_types):
        if t == 1:
            Processing_time.append(CKS_Type1)
            J[i + 1] = 5
        elif t == 2:
            Processing_time.append(CKS_Type2)
            J[i + 1] = 8
        else:
            Processing_time.append(CKS_Type3)
            J[i + 1] = 10

    O_num = sum(J.values())
    Arrival_Time = sorted([random.randint(0, 20000) for _ in range(J_num)])
    Due_Dates = [Arrival_Time[i] + J[i + 1] * random.randint(150, 250) for i in range(J_num)]

    Breakdowns = []
    for _ in range(50):
        m = random.randint(0, M_num - 1)
        s = random.randint(1000, 25000)
        d = random.randint(50, 200)
        Breakdowns.append({'machine': m, 'start': s, 'duration': d})

elif SCENARIO == 8:
    # KỊCH BẢN 8: NHỮNG ĐỢT SÓNG QUÁ TẢI (BURST & SHOCK)
    random.seed(108)
    J_num = 1200
    M_num = 20
    Job_types = random.choices([1, 2, 3], weights=[0.3, 0.4, 0.3], k=J_num)
    Processing_time = []
    J = {}
    for i, t in enumerate(Job_types):
        if t == 1:
            Processing_time.append(CKS_Type1); J[i + 1] = 5
        elif t == 2:
            Processing_time.append(CKS_Type2); J[i + 1] = 8
        else:
            Processing_time.append(CKS_Type3); J[i + 1] = 10
    O_num = sum(J.values())

    Arrival_Time = []
    for i in range(J_num):
        if i < 300:
            Arrival_Time.append(0)
        elif i < 600:
            Arrival_Time.append(5000)
        elif i < 900:
            Arrival_Time.append(10000)
        else:
            Arrival_Time.append(15000)

    Due_Dates = [Arrival_Time[i] + J[i + 1] * random.randint(80, 150) for i in range(J_num)]

    Breakdowns = []
    for wave_time in [1000, 6000, 11000, 16000]:
        for _ in range(20):
            m = random.randint(0, M_num - 1)
            s = wave_time + random.randint(0, 2000)
            d = random.randint(100, 300)
            Breakdowns.append({'machine': m, 'start': s, 'duration': d})

elif SCENARIO == 9:
    # KỊCH BẢN 9: ĐỊA NGỤC TRỄ HẠN (TARDINESS HELL)
    random.seed(109)
    J_num = 1500
    M_num = 20
    Job_types = random.choices([1, 2, 3], weights=[0.5, 0.3, 0.2], k=J_num)
    Processing_time = []
    J = {}
    for i, t in enumerate(Job_types):
        if t == 1:
            Processing_time.append(CKS_Type1); J[i + 1] = 5
        elif t == 2:
            Processing_time.append(CKS_Type2); J[i + 1] = 8
        else:
            Processing_time.append(CKS_Type3); J[i + 1] = 10
    O_num = sum(J.values())

    Arrival_Time = sorted([random.randint(0, 25000) for _ in range(J_num)])
    Due_Dates = []
    for i in range(J_num):
        if random.random() < 0.3:  # 30% Đơn hàng hỏa tốc
            Due_Dates.append(Arrival_Time[i] + J[i + 1] * random.randint(20, 50))
        else:
            Due_Dates.append(Arrival_Time[i] + J[i + 1] * random.randint(100, 200))

    Breakdowns = []
    for _ in range(100):
        m = random.randint(0, M_num - 1)
        s = random.randint(500, 30000)
        d = random.randint(150, 400)
        Breakdowns.append({'machine': m, 'start': s, 'duration': d})

# ==========================================
# NHÓM 3 (KỊCH BẢN 10-12): QUY MÔ CÔNG NGHIỆP SIÊU LỚN (>5000 Jobs)
# Mục đích: Stress-test cho ATC và GP. (TUYỆT ĐỐI KHÔNG CHẠY BẰNG GA)
# ==========================================

elif SCENARIO == 10:
    # KỊCH BẢN 10: SIÊU QUY MÔ (EXTREME SCALE)
    random.seed(42)
    J_num = 5000
    M_num = 20
    Job_types = random.choices([1, 2, 3], weights=[0.4, 0.4, 0.2], k=J_num)
    Processing_time = []
    J = {}
    for i, t in enumerate(Job_types):
        if t == 1:
            Processing_time.append(CKS_Type1); J[i + 1] = 5
        elif t == 2:
            Processing_time.append(CKS_Type2); J[i + 1] = 8
        else:
            Processing_time.append(CKS_Type3); J[i + 1] = 10
    O_num = sum(J.values())

    Arrival_Time = [random.randint(0, 100000) for _ in range(J_num)]
    Due_Dates = [Arrival_Time[i] + J[i + 1] * random.randint(150, 300) for i in range(J_num)]

    Breakdowns = []
    for _ in range(200):
        m = random.randint(0, M_num - 1)
        s = random.randint(1000, 100000)
        d = random.randint(100, 500)
        Breakdowns.append({'machine': m, 'start': s, 'duration': d})

elif SCENARIO == 11:
    # KỊCH BẢN 11: THẢM HỌA MÁY HỎNG (CATASTROPHE)
    random.seed(99)
    J_num = 5500
    M_num = 20
    Job_types = random.choices([1, 2, 3], weights=[0.33, 0.33, 0.34], k=J_num)
    Processing_time = []
    J = {}
    for i, t in enumerate(Job_types):
        if t == 1:
            Processing_time.append(CKS_Type1); J[i + 1] = 5
        elif t == 2:
            Processing_time.append(CKS_Type2); J[i + 1] = 8
        else:
            Processing_time.append(CKS_Type3); J[i + 1] = 10
    O_num = sum(J.values())

    Arrival_Time = sorted([random.randint(0, 40000) for _ in range(J_num)])
    Due_Dates = [Arrival_Time[i] + J[i + 1] * random.randint(30, 80) for i in range(J_num)]

    Breakdowns = []
    for _ in range(1000):  # 1000 sự cố
        m = random.randint(0, M_num - 1)
        s = random.randint(500, 60000)
        d = random.randint(80, 400)
        Breakdowns.append({'machine': m, 'start': s, 'duration': d})

elif SCENARIO == 12:
    # KỊCH BẢN 12: NÚT THẮT CỔ CHAI & ĐỢT SÓNG ĐƠN HÀNG (BOTTLENECK & SURGES)
    random.seed(2026)
    J_num = 6000
    M_num = 20

    CKS_BOTTLE = []
    for row in CKS_Type2:
        CKS_BOTTLE.append([p * 5 if i < 3 and p != 9999 else p for i, p in enumerate(row)])

    Job_types = random.choices([1, 2], weights=[0.2, 0.8], k=J_num)
    Processing_time = []
    J = {}
    for i, t in enumerate(Job_types):
        if t == 1:
            Processing_time.append(CKS_Type1); J[i + 1] = 5
        else:
            Processing_time.append(CKS_BOTTLE); J[i + 1] = 8
    O_num = sum(J.values())

    Arrival_Time = []
    for i in range(J_num):
        if i % 1000 < 500:
            Arrival_Time.append((i // 1000) * 15000)
        else:
            Arrival_Time.append((i // 1000) * 15000 + random.randint(100, 10000))

    Due_Dates = [Arrival_Time[i] + J[i + 1] * random.randint(80, 200) for i in range(J_num)]

    Breakdowns = []
    for _ in range(300):
        m = random.choice([0, 1, 2, random.randint(3, M_num - 1)])
        s = random.randint(1000, 80000)
        d = random.randint(200, 600)
        Breakdowns.append({'machine': m, 'start': s, 'duration': d})