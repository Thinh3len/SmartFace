
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import urllib.request
import os
import database

# =============================================
# BUOC 1 — NHAP ID VA KIEM TRA DB
# =============================================

person_id = input("Nhap ma nguoi dung: ")

if not database.person_exists(person_id):
    print("Khong tim thay nguoi nay trong he thong!")
    print("Hay chay qr_scan.py de quet QR truoc.")
    exit()

print(f"Tim thay: {person_id} — Chuan bi chup anh...")

# =============================================
# BUOC 2 — TAI MODEL AI (chi tai 1 lan duy nhat)
# =============================================

model_path = 'face_landmarker.task'

if not os.path.exists(model_path):
    print("Dang tai model AI tu Google, vui long doi...")
    url = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
    urllib.request.urlretrieve(url, model_path)
    print("Tai model xong!")

# =============================================
# BUOC 3 — CAU HINH BO NHAN DIEN MAT
# =============================================

base_options = python.BaseOptions(model_asset_path=model_path)

options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    output_face_blendshapes=False,
    output_facial_transformation_matrixes=False,
    num_faces=1
)

detector = vision.FaceLandmarker.create_from_options(options)

# =============================================
# BUOC 4 — MO CAMERA
# =============================================

cap = cv2.VideoCapture(0)
face_crop = None

print("Camera san sang!")
print("Nhan SPACE de chup anh | Nhan Q de thoat")

# =============================================
# BUOC 5 — VONG LAP CAMERA
# =============================================

while True:

    # Doc frame tu camera
    ret, frame = cap.read()
    if not ret:
        print("Loi camera!")
        break

    # Lat guong cho tu nhien
    frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]

    # Chuyen BGR sang RGB de dua vao mediapipe
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    )

    # Detect mat
    result = detector.detect(mp_image)
    face_crop = None

    # Neu tim thay mat
    if result.face_landmarks:

        # Lay 478 diem landmark cua mat dau tien
        landmarks = result.face_landmarks[0]

        # Lay toa do x, y cua tat ca diem landmark
        xs = [int(lm.x * w) for lm in landmarks]
        ys = [int(lm.y * h) for lm in landmarks]

        # Ve cac diem landmark len mat
        for cx, cy in zip(xs, ys):
            cv2.circle(frame, (cx, cy), 1, (0, 255, 0), -1)

        # Tinh vung bao quanh mat
        x1 = max(0, min(xs) - 30)
        y1 = max(0, min(ys) - 30)
        x2 = min(w, max(xs) + 30)
        y2 = min(h, max(ys) + 30)

        # Cat vung mat ra khoi frame
        face_crop = frame[y1:y2, x1:x2]

        # Ve khung xanh xung quanh mat
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Hien chu huong dan
    cv2.putText(frame, f"Nguoi dung: {person_id}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    if face_crop is not None:
        cv2.putText(frame, "Nhan SPACE de chup", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Chua thay mat!", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Hien frame len man hinh
    cv2.imshow("Chup Anh Khuon Mat", frame)

    # =============================================
    # BUOC 6 — XU LY PHIM BAM
    # =============================================

    key = cv2.waitKey(1) & 0xFF

    # Bam SPACE de chup anh
    if key == 32:
        if face_crop is None:
            print("Chua thay mat, hay nhin vao camera!")
        else:
            # Nen anh thanh bytes de luu vao SQLite
            success, buffer = cv2.imencode('.jpg', face_crop)

            if success:
                # Ép kiểu bytes an toàn tránh lỗi AttributeError cũ
                img_bytes = bytes(buffer)
                database.save_face(person_id, img_bytes)
                print(f"Da luu anh khuon mat cho: {person_id}")
                
                # --- CHỨC NĂNG THÊM THEO YÊU CẦU ---
                # Xóa màn hình vẽ chữ thông báo thành công trực quan
                cv2.rectangle(frame, (0, 0), (w, h), (0, 0, 0), -1)
                cv2.putText(frame, "CHUP ANH HOAN THANH!", (int(w/2) - 180, int(h/2)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                cv2.imshow("Chup Anh Khuon Mat", frame)
                cv2.waitKey(2000) # Đóng băng màn hình 2 giây để hiển thị chữ rồi tự thoát
                break
            else:
                print("Loi khi xu ly anh, thu lai!")

    # Bam Q de thoat
    elif key == ord('q'):
        print("Da thoat.")
        break

# =============================================
# BUOC 7 — DONG CAMERA
# =============================================

cap.release()
cv2.destroyAllWindows()
print("Hoan thanh!")