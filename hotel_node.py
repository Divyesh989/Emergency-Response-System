import customtkinter as ctk
import firebase_admin
from firebase_admin import credentials, db
import time

FIREBASE_DB_URL = "https://smart-help-9eec0-default-rtdb.asia-southeast1.firebasedatabase.app" 
SERVICE_ACCOUNT_FILE = r"B:\Solution Challange 2026\service-key.json"

if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_FILE)
    firebase_admin.initialize_app(cred, {'databaseURL': FIREBASE_DB_URL})

class SentinelTactical(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sentinel Tactical Command - Venue Node")
        self.geometry("1100x700")
        
        self.current_floor = 1
        self.selected_zone = None
        
        self.layouts = {
            1: ["Lobby", "Swimming Pool", "Dining Hall", "Reception", "Valet", "Main Entrance"],
            2: ["Gym", "Dining Area", "Locker Room", "Cardio Zone", "Staff Room", "Service Lift"],
            "default": [f"Room {i+100}" for i in range(1, 7)] + ["Utility Room", "Service Closet", "Fire Exit"]
        }

        self.setup_ui()

    def setup_ui(self):
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        self.floor_frame = ctk.CTkFrame(self, width=180)
        self.floor_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(self.floor_frame, text="LEVELS", font=("Arial", 18, "bold")).pack(pady=10)
        
        for i in range(10, 0, -1):
            color = "#1f538d" if i == self.current_floor else "#333333"
            btn = ctk.CTkButton(self.floor_frame, text=f"FLOOR {i}", 
                                command=lambda f=i: self.change_floor(f),
                                fg_color=color)
            btn.pack(pady=3, padx=15, fill="x")

        self.map_frame = ctk.CTkFrame(self)
        self.map_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.floor_title = ctk.CTkLabel(self.map_frame, text="FLOOR 1: MAIN LEVEL", font=("Arial", 22, "bold"))
        self.floor_title.pack(pady=15)

        self.grid_container = ctk.CTkFrame(self.map_frame, fg_color="transparent")
        self.grid_container.pack(expand=True, fill="both", padx=30, pady=10)
        self.render_map()

        self.control_frame = ctk.CTkFrame(self, width=280)
        self.control_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(self.control_frame, text="REPORT INCIDENT", font=("Arial", 16, "bold")).pack(pady=15)
        
        ctk.CTkButton(self.control_frame, text="🔥 FIRE", fg_color="#990000", height=45,
                      command=lambda: self.send_report("FIRE")).pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(self.control_frame, text="⚕️ MEDICAL", fg_color="#006600", height=45,
                      command=lambda: self.send_report("MEDICAL")).pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(self.control_frame, text="🛡️ SECURITY", fg_color="#000066", height=45,
                      command=lambda: self.send_report("SECURITY")).pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(self.control_frame, text="📋 VIEW ALL INCIDENTS", fg_color="#555555", height=45,
                      command=self.open_log_window).pack(pady=10, padx=20, fill="x")

        self.status_bar = ctk.CTkLabel(self.control_frame, text="System Ready", text_color="gray")
        self.status_bar.pack(side="bottom", pady=20)

    def render_map(self):
        for widget in self.grid_container.winfo_children():
            widget.destroy()
            
        zones = self.layouts.get(self.current_floor, self.layouts["default"])
        self.zone_btns = {}
        
        for i, zone in enumerate(zones):
            r, c = divmod(i, 3)
            btn = ctk.CTkButton(self.grid_container, text=zone, height=140,
                                fg_color="#2B2B2B", border_width=1,
                                command=lambda z=zone: self.select_zone(z))
            btn.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
            self.zone_btns[zone] = btn
            
        for i in range(3):
            self.grid_container.grid_columnconfigure(i, weight=1)
            self.grid_container.grid_rowconfigure(i, weight=1)

    def change_floor(self, f):
        self.current_floor = f
        suffix = "MAIN" if f==1 else "FITNESS/DINING" if f==2 else "GUEST ROOMS"
        self.floor_title.configure(text=f"FLOOR {f}: {suffix}")
        self.selected_zone = None
        self.render_map()

        for widget in self.floor_frame.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.configure(fg_color="#1f538d" if widget.cget("text") == f"FLOOR {f}" else "#333333")

    def select_zone(self, zone):
        self.selected_zone = zone
        for name, btn in self.zone_btns.items():
            btn.configure(fg_color="#1F538D" if name == zone else "#2B2B2B")

    def send_report(self, itype):
        if not self.selected_zone:
            self.status_bar.configure(text="❌ SELECT ZONE", text_color="red")
            return
            
        data = {
            "report_text": f"{itype} emergency at {self.selected_zone} (Floor {self.current_floor})",
            "floor": self.current_floor,
            "zone": self.selected_zone,
            "type": itype,
            "timestamp": int(time.time()),
            "hotel_name": "Grand Plaza Resort"
        }
        db.reference('raw_reports').push(data)
        self.status_bar.configure(text="✔ BROADCASTED", text_color="green")

    def open_log_window(self):
        log_win = ctk.CTkToplevel(self)
        log_win.title("Active Incident Logs")
        log_win.geometry("500x400")
        log_win.attributes("-topmost", True) # Keep on top
        
        txt = ctk.CTkTextbox(log_win, width=480, height=380)
        txt.pack(padx=10, pady=10)
        
        logs = db.reference('raw_reports').order_by_key().limit_to_last(10).get()
        if logs:
            for entry in reversed(list(logs.values())):
                txt.insert("end", f"[{entry['type']}] {entry['zone']} (F{entry['floor']}) - {entry['report_text']}\n\n")
        else:
            txt.insert("end", "No incidents reported.")

if __name__ == "__main__":
    app = SentinelTactical()
    app.mainloop()