import socket
import json
import time

def send_dispatch_command(target_ip, target_port, user_name, bpm_value):
    """Đóng gói dữ liệu sinh hiệu và gửi lệnh điều khiển sang Xe Tự Hành qua mạng LAN"""
    # Khởi tạo Socket kết nối TCP/IP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(3.0) # Thời gian chờ kết nối tối đa 3 giây
    
    # Đóng gói gói tin JSON chứa dữ liệu phân tích từ AI
    payload = {
        "device_source": "MAIN_KITCHEN_HUB",
        "timestamp": time.time(),
        "user_profile": user_name,
        "vitals": {
            "heart_rate_bpm": int(bpm_value)
        },
        "action_required": "DEPLOY_MOBILE_VEHICLE",
        "payload_recommendation": "Chilled Mineral Water & Fresh Berries"
    }
    
    try:
        print(f"[Hub Server] Attempting to connect to Mobile Vehicle at {target_ip}:{target_port}...")
        client_socket.connect((target_ip, target_port))
        
        # Chuyển đổi gói tin JSON sang định dạng chuỗi mã hóa UTF-8 để truyền qua mạng
        json_data = json.dumps(payload)
        client_socket.sendall(json_data.encode('utf-8'))
        print(f"[Hub Server] 🚀 Successfully sent dispatch command for {user_name} (BPM: {int(bpm_value)})")
        
    except socket.timeout:
        print("[Hub Server] ❌ Error: Connection timed out. Is the Mobile Vehicle online?")
    except Exception as e:
        print(f"[Hub Server] ❌ Connection failed: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    # Địa chỉ IP giả lập chạy ngay trên máy tính của bạn (Localhost)
    # Khi chạy thực tế, bạn sẽ đổi thành IP mạng Wi-Fi của Raspberry Pi trên Xe Tự Hành
    VEHICLE_IP = "127.0.0.1" 
    VEHICLE_PORT = 8585
    
    print("=== AI_BioFridge: Simulated Hub Telemetry Transmitter ===")
    time.sleep(1)
    
    # Giả lập tình huống AI phát hiện anh Minh có nhịp tim cao (88 BPM) do mệt mỏi
    send_dispatch_command(VEHICLE_IP, VEHICLE_PORT, "John (Father)", 88)
