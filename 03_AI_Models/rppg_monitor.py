import cv2
import mediapipe as mp
import numpy as np

def main():
    # Khởi tạo công nghệ nhận diện khuôn mặt của Google Mediapipe
    mp_face_detection = mp.solutions.face_detection
    mp_drawing = mp.solutions.drawing_utils
    
    # Mở camera mặc định của máy tính (hoặc tủ lạnh)
    cap = cv2.VideoCapture(0)
    
    print("=== AI_BioFridge: Hệ thống quét rPPG đang khởi động ===")
    print("Nhấn 'q' để thoát ứng dụng.")

    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Không tìm thấy Camera.")
                break

            # Chuyển đổi màu từ BGR sang RGB để AI xử lý chính xác hơn
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_detection.process(image_rgb)

            # Nếu phát hiện thấy khuôn mặt của chủ nhà
            if results.detections:
                for detection in results.detections:
                    # Lấy tọa độ khung vị trí khuôn mặt
                    bboxC = detection.location_data.relative_bounding_box
                    ih, iw, _ = image.shape
                    x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                    
                    # Giới hạn vùng trán/má để thu thập dữ liệu màu sắc da (ROI - Region of Interest)
                    roi = image[max(0, y):min(ih, y+h), max(0, x):min(iw, x+w)]
                    
                    if roi.size > 0:
                        # Phân tích kênh màu Xanh Lá (Green) - kênh nhạy cảm nhất với mạch máu dưới da
                        mean_green = np.mean(roi[:, :, 1])
                        
                        # Hiển thị thông số thô lên màn hình (Tiền đề để thuật toán lọc ra nhịp tim bpm)
                        cv2.putText(image, f"Scanning Biomarkers... G-Signal: {mean_green:.2f}", 
                                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    
                    # Vẽ khung nhận diện quanh mặt chủ nhà
                    mp_drawing.draw_detection(image, detection)

            # Hiển thị luồng video thời gian thực trên màn hình tủ lạnh
            cv2.imshow('AI_BioFridge - Contactless rPPG Monitor', image)

            # Nhấn nút 'q' để tắt camera
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
