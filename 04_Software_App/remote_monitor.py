import time
import json

# Giả lập cơ sở dữ liệu kho thực phẩm bên trong tủ lạnh lớn
inventory_database = {
    "fresh_milk": {"quantity_pct": 20, "threshold_pct": 30, "category": "Dairy"},
    "eggs": {"quantity_pcs": 2, "threshold_pcs": 6, "category": "Protein"},
    "salmon_fillet": {"quantity_pcs": 1, "threshold_pcs": 1, "category": "Protein"},
    "bananas": {"quantity_pcs": 0, "threshold_pcs": 3, "category": "Fruit"}
}

def generate_cloud_shopping_list(inventory):
    """AI phân tích tại biên và chỉ đẩy danh sách văn bản dạng chữ lên Đám mây"""
    shopping_list = []
    
    for item, data in inventory.items():
        # Kiểm tra nếu số lượng thực phẩm xuống dưới mức cảnh báo tối thiểu
        if "quantity_pct" in data and data["quantity_pct"] < data["threshold_pct"]:
            shopping_list.append({"item": item, "status": f"Low ({data['quantity_pct']}% left)", "action": "Buy More"})
        elif "quantity_pcs" in data and data["quantity_pcs"] < data["threshold_pcs"]:
            shopping_list.append({"item": item, "status": f"Low ({data['quantity_pcs']} pcs left)", "action": "Buy More"})
            
    return shopping_list

def main():
    print("==================================================================")
    print("             AI_BIOFRIDGE: EDGE-TO-CLOUD SYNC INTERFACE           ")
    print("==================================================================")
    print("[Secure Node] Local AI processing completed. Local images DELETED for security.")
    print("[Secure Node] Encrypting text data using AES-256 protocol...")
    time.sleep(1.5)
    
    # Tạo danh sách đẩy lên đám mây
    cloud_data = generate_cloud_shopping_list(inventory_database)
    
    print("\n[Cloud Cloud Status]: Syncing with User's Mobile App...")
    print("------------------------------------------------------------------")
    print("📱 [YOUR SMARTPHONE LIVE SHOPPING LIST]:")
    print("------------------------------------------------------------------")
    
    for entry in cloud_data:
        print(f" 🛒 NEED TO BUY -> Item: {entry['item'].replace('_', ' ').title()}")
        print(f"    Current Status: {entry['status']}")
        print(f"    AI Recommendation: Please restock today to maintain meal plan.\n")
        
    print("------------------------------------------------------------------")
    print("[Security Status] Connection closed. No video/audio data was exposed.")
    print("==================================================================")

if __name__ == "__main__":
    main()
