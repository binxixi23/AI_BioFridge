import cv2
import mediapipe as mp
import numpy as np
import serial
import threading
import json
from scipy.signal import butter, lfilter

# ==============================================================================
# PHẦN 1: THUẬT TOÁN XỬ LÝ TÍN HIỆU SỐ CHUYÊN SÂU (DSP FOR rPPG)
# ==============================================================================

def butter_bandpass(lowcut, highcut, fs, order=5):
    """Khởi tạo bộ lọc cấu hình Butterworth băng thông"""
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    """Áp dụng bộ lọc dải tần lên chuỗi biến động màu sắc của da mặt"""
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def calculate_bpm(signal_buffer, fs):
    """Tính toán chỉ số nhịp tim bằng Biến đổi Fourier nhanh (FFT)"""
    if len(signal_buffer) < 64:  # Cần tối thiểu dữ liệu để phân tích tần số
        return 0
        
    # 1. Chuẩn hóa khử nhiễu ánh sáng nền (Zero-mean và Unit-variance)
    signal_norm = (signal_buffer - np.mean(signal_buffer)) / np.std(signal_buffer)
    
    # 2. Lọc băng thông (Giới hạn tần số nhịp tim người từ 0.75Hz đến 3.0Hz ~ 45-180 BPM)
    filtered_signal = butter_bandpass_filter(signal_norm, 0.75, 3.0, fs, order=4)
    
    # 3. Thực hiện biến đổi FFT sang miền tần số
    n = len(filtered_signal)
    fft_data = np.abs(np.fft.rfft(filtered_signal))
    fft_freqs = np.fft.rfftfreq(n, d=1/fs)
    
    # 4. Tìm tần số có biên độ mạnh nhất trong dải tần hợp lệ
    valid_idx = np.where((fft_freqs >= 0.75) & (fft_freqs <= 3.0))
    if len(valid_idx) == 0 or len(valid_idx[0]) == 0:
        return 0
        
    peak_idx = valid_idx[0][np.argmax(fft_data[valid_idx])]
    heart_rate_hz = fft_freqs[peak_idx]
    
    # Quy đổi tần số Hz sang chỉ số nhịp tim theo phút (BPM)
    bpm = heart_rate_hz * 60
    return bpm

# ==============================================================================
# PHẦN 2: LUỒNG GIÁM SÁT PHẦN CỨNG NGỬI MÙI (E-NOSE SERIAL THREAD)
# ==============================================================================

# Biến toàn cầu để lưu trạng thái không khí từ cảm biến gửi về
latest_enose_data = "Waiting for E-Nose..."

def arduino_serial_listener(com_port="COM3", baudrate=115200):
    """Luồng chạy ngầm liên tục đọc dữ liệu khí Gas/Ethylene từ cổng USB Arduino"""
    global latest_enose_data
    try:
        # Mở cổng kết nối với mạch vi điều khiển
        ser = serial.Serial(com_port, baudrate, timeout=1)
        print(f"\n[Hardware Thread] Connected successfully to E-Nose on {com_port}")
        
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line:
                try:
                    # Giải mã chuỗi dữ liệu JSON từ C++ truyền lên
                    data_packet = json.loads(line)
                    eth_ratio = data_packet.get("ethylene_methane_ratio", 1.0)
                    voc_ratio = data_packet.get("ammonia_voc_ratio", 1.0)
                    
                    # Lưu thông tin định dạng ngắn gọn để hiển thị lên màn hình camera
                    latest_enose_data = f"E-Nose VOC: {voc_ratio:.2f} | Ethylene: {eth_ratio:.2f}"
                    
                    # Thuật toán AI phân tích nồng độ khí cảnh báo đồ hỏng
                    if eth_ratio < 0.5:
                        print("🚨 [AI Hardware Warning] Ethylene spike detected! Fruit spoilage imminent.")
                except json.JSONDecodeError:
                    pass # Bỏ qua nếu dòng dữ liệu truyền bị khuyết dòng do xung đột phần cứng
                    
    except Exception as e:
        latest_enose_data = "E-Nose Offline (Check USB Connection)"
        print(f"\n[Hardware Thread] Could not open serial port {com_port}: {e}")

# ==============================================================================
# PHẦN 3: GIAO DIỆN CAMERA AI CHÍNH CỦA TỦ LẠNH (MAIN EXECUTION LOOP)
# ==============================================================================

def main():
    global latest_enose_data
    
    # Khởi động luồng đọc cảm biến phần cứng chạy song song để không làm lag camera
    hardware_thread = threading.Thread(target=arduino_serial_listener, args=("COM3", 115200), daemon=True)
    hardware_thread.start()

    # Cấu hình hệ thống nhận diện Face Mesh siêu chính xác của Google
    mp_face_mesh = mp.solutions.face_mesh
    cap = cv2.VideoCapture(0)
    
    # Quản lý bộ đệm tín hiệu thời gian thực cho rPPG
    signal_buffer = []
    buffer_size = 150  # Lưu giữ ~5 giây dữ liệu ở tốc độ 30 FPS
    fps = 30.0         # Tốc độ quét mục tiêu
    current_bpm = 0
    frame_counter = 0

    print("\n=== AI_BioFridge: Hệ thống Tích hợp Toàn diện (rPPG + E-Nose) đang chạy ===")
    print("Vui lòng hướng mặt về camera để hiệu chuẩn sinh hiệu.")
    print("Nhấn 'q' để tắt ứng dụng.")

    with mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.6) as face_mesh:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Lỗi: Không nhận được tín hiệu hình ảnh từ Camera.")
                break

            frame_counter += 1
            h_img, w_img, _ = image.shape
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(image_rgb)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    # Lấy tọa độ các điểm mốc vùng má (mao mạch dày đặc) để trích xuất tín hiệu nhịp tim
                    lm = face_landmarks.landmark
                    x1, y1 = int(lm[117].x * w_img), int(lm[117].y * h_img)
                    x2, y2 = int(lm[346].x * w_img), int(lm[346].y * h_img)
                    
                    # Cắt vùng da mặt cần phân tích (Region of Interest)
                    roi = image[min(y1, y2):max(y1, y2), min(x1, x2):max(x1, x2)]
                    
                    if roi.size > 0:
                        # Lấy giá trị trung bình của kênh màu Xanh lá (Green Channel)
                        mean_green = np.mean(roi[:, :, 1])
                        signal_buffer.append(mean_green)
                        
                        # Giới hạn kích thước bộ đệm theo nguyên tắc FIFO
                        if len(signal_buffer) > buffer_size:
                            signal_buffer.pop(0)
                        
                        # Cập nhật tính toán nhịp tim BPM sau mỗi 15 khung hình (0.5 giây)
                        if frame_counter % 15 == 0 and len(signal_buffer) >= 64:
                            calculated = calculate_bpm(signal_buffer, fps)
                            if 45 <= calculated <= 180:
                                current_bpm = calculated

                        # Vẽ hộp Neon quét tế bào biểu bì da quanh má
                        cv2.rectangle(image, (min(x1, x2), min(y1, y2)), (max(x1, x2), max(y1, y2)), (255, 255, 0), 2)
                        
                        # In chỉ số nhịp tim quét được lên luồng video
                        status_text = f"AI Pulse: {int(current_bpm)} BPM" if current_bpm > 0 else "Calibrating Vitals..."
                        cv2.putText(image, status_text, (min(x1, x2), min(y1, y2) - 10), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # --- HIỂN THỊ THÔNG TIN PHẦN CỨNG LÊN GIAO DIỆN TỦ LẠNH ---
            # Đè thanh trạng thái cảm biến ngửi mùi (E-Nose) thu thập từ luồng chạy ngầm lên góc trên cùng màn hình
            cv2.rectangle(image, (5, 5), (480, 35), (0, 0, 0), -1)
            cv2.putText(image, latest_enose_data, (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

            # Bật cửa sổ camera HUD của tủ lạnh
            cv2.imshow('AI_BioFridge - Integrated Bio & Chemical Monitor HUD', image)

            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
