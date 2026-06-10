import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_dashboard():
    clear_screen()
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
    print("   - Shelf 1 (Dairy) : Fresh Milk (Capacity: 45%) - Expiry: 2 Days!")
    print("   - Crisper (Fruits): Bananas (Ethylene Level: High) - Consume within 24h.")
    print("   - Drawer (Protein): Fresh Salmon (E-Nose Metric: SAFE)")
    print("------------------------------------------------------------------")
    print(" [PART 2: AUTONOMOUS MOBILE VEHICLE STATUS]")
    print("   - Deployment State: MOVING TO LIVING ROOM SOFA")
    print("   - Power Connection: Tethered Cable Reel Engaged (Length Out: 3.4m)")
    print("   - Internal Payload: Chilled Mineral Water & Fresh Berries")
    print("------------------------------------------------------------------")
    print(" [AI PROACTIVE ALERT]")
    print(" 👉 'Mobile cooling vehicle dispatched to your sofa. Refreshments ready.'")
    print("==================================================================")

def main():
    try:
        while True:
            display_dashboard()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nAI_BioFridge Dashboard Closed Successfully.")

if __name__ == "__main__":
    main()
