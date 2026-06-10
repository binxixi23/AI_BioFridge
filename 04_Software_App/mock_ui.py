import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Giả lập cơ sở dữ liệu thực phẩm thời gian thực bên trong tủ lạnh lớn
# Hệ thống AI tự động giám sát số lượng (Quantity) so với ngưỡng tối thiểu (Threshold)
inventory_data = {
    "Fresh Milk": {"qty": 20, "thresh": 30, "unit": "%", "status": "Low!"},
    "Eggs": {"qty": 2, "thresh": 6, "unit": "pcs", "status": "Critical!"},
    "Fresh Salmon": {"qty": 1, "thresh": 1, "unit": "pcs", "status": "Safe"},
    "Bananas": {"qty": 0, "thresh": 3, "unit": "pcs", "status": "Empty!"},
    "Broccoli": {"qty": 100, "thresh": 50, "unit": "%", "status": "Optimal"}
}

def generate_shopping_list():
    """Thuật toán AI trích xuất các mặt hàng cần mua thêm dựa trên ngưỡng số lượng"""
    shopping_list = []
    for food, metrics in inventory_data.items():
        if metrics["qty"] < metrics["thresh"]:
            shopping_list.append(f"{food} ({metrics['status']} - Only {metrics['qty']}{metrics['unit']} left)")
    return shopping_list

def display_dashboard():
    clear_screen()
    shopping_list = generate_shopping_list()
    
    print("==================================================================")
    print("                AI_BIOFRIDGE CENTRAL CONTROL HUB                  ")
    print("==================================================================")
    print(f" TIME: {time.strftime('%Y-%m-%d %H:%M:%S')} | MAIN HUB: ONLINE  | MOBILE VEHICLE: READY ")
    print("------------------------------------------------------------------")
    print(" [USER HEALTH MONITOR]")
    print("   - Active Profile  : John (Father)")
    print("   - Current Vitals  : 74 BPM via rPPG (Normal Range)")
    print("   - AI Evaluation   : Elevating fatigue detected. Replenishment advised.")
    print("------------------------------------------------------------------")
    print(" [PART 1: MAIN KITCHEN REFRIGERATOR INVENTORY]")
    print(f"   - Shelf 1 (Dairy) : Fresh Milk ({inventory_data['Fresh Milk']['qty']}{inventory_data['Fresh Milk']['unit']}) - Expiry: 2 Days!")
    print(f"   - Crisper (Fruits): Bananas ({inventory_data['Bananas']['qty']}{inventory_data['Bananas']['unit']}) - Out of stock.")
    print(f"   - Drawer (Protein): Fresh Salmon (E-Nose Metric: SAFE)")
    print("------------------------------------------------------------------")
    print(" [PART 2: AUTONOMOUS MOBILE VEHICLE STATUS]")
    print("   - Deployment State: MOVING TO LIVING ROOM SOFA")
    print("   - Power Connection: Tethered Cable Reel Engaged (Length Out: 3.4m)")
    print("   - Internal Payload: Chilled Mineral Water & Fresh Berries")
    print("------------------------------------------------------------------")
    print(" 📱 [AUTOMATED CLOUD SHOPPING LIST FOR YOUR SMARTPHONE]")
    
    if len(shopping_list) > 0:
        for index, item in enumerate(shopping_list, 1):
            print(f"   {index}. 🛒 Need to restock: {item}")
    else:
        print("   ✅ Inventory optimal. No restocking needed today.")
        
    print("------------------------------------------------------------------")
    print(" [AI PROACTIVE ALERT]")
    print(" 👉 'Mobile cooling vehicle dispatched to your sofa. Refreshments ready.'")
    print("==================================================================")

def main():
    try:
        while True:
            display_dashboard()
            time.sleep(2) # Cập nhật giao diện tự động sau mỗi 2 giây
    except KeyboardInterrupt:
        print("\nAI_BioFridge Dashboard Closed Successfully.")

if __name__ == "__main__":
    main()
