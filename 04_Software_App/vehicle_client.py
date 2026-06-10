import socket
import json

def start_vehicle_listener(host_ip, host_port):
    """Khởi động luồng lắng nghe lệnh từ Tủ lạnh lớn để kích hoạt chu trình di chuyển"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Cấu hình cho phép tái sử dụng cổng mạng tránh lỗi nghẽn mạch
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host_ip, host_port))
    server_socket.listen(5)
    
    print(f"[Vehicle Client] 🖥️ Autonomous Vehicle Listener active on {host_ip}:{host_port}")
    print("[Vehicle Client] Waiting for commands from Main AI Hub...")

    try:
        while True:
            # Chấp nhận kết nối từ Tủ lạnh lớn
            connection, client_address = server_socket.accept()
            try:
                # Nhận gói tin truyền tải dữ liệu dung lượng tối đa 4096 bytes
                data = connection.recv(4096)
                if data:
                    # Giải mã chuỗi JSON từ Hub gửi sang
                    command_packet = json.loads(data.decode('utf-8'))
                    
                    # Trích xuất dữ liệu phân tích sinh hiệu từ gói tin
                    user = command_packet["user_profile"]
                    bpm = command_packet["vitals"]["heart_rate_bpm"]
                    item = command_packet["payload_recommendation"]
                    
                    print("\n==================================================================")
                    print("🚨 [ALERT: INCOMING TELEMETRY FROM MAIN HUB]")
                    print(f"👉 Target User Located : {user}")
                    print(f"👉 Biometric Alert     : Elevated Stress Detected ({bpm} BPM)")
                    print(f"👉 Auto-Reel Status    : Power Tether Engaged, Unspooling Cable...")
                    print(f"👉 Mission Profile     : Delivering [{item}] to Living Room Sofa")
                    print("==================================================================")
                    print("[Vehicle Client] 🏎️ AGV Drive system active. Moving out now...")
                    
            except Exception as e:
                print(f"[Vehicle Client] Error processing data: {e}")
            finally:
                connection.close()
                
    except KeyboardInterrupt:
        print("\n[Vehicle Client] Shuttling down Listener systems safely.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    LISTEN_IP = "127.0.0.1" # Lắng nghe cục bộ trên máy tính
    LISTEN_PORT = 8585
    start_vehicle_listener(LISTEN_IP, LISTEN_PORT)
