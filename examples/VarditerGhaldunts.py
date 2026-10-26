import tkinter as tk
from tkinter import messagebox
from pymavlink import mavutil


class DroneGCSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drone Ground Control Station")
        self.root.geometry("400x560")
        self.root.config(bg="#2b2b2b")

        self.master = None
        self.mode_buttons = []

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        tk.Label(root, text="DRONE CONTROL PANEL", bg="#2b2b2b", fg="#ffffff", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(root, text="Connection String:", bg="#2b2b2b", fg="#cccccc", font=("Arial", 11)).pack(anchor="w",padx=30)
        self.entry_conn = tk.Entry(root, width=28, font=("Arial", 12))
        self.entry_conn.insert(0, "udp:127.0.0.1:14550")
        self.entry_conn.pack(pady=5)

        self.btn_connect = tk.Button(root, text="Connect", bg="#2e7d32", fg="white", font=("Arial", 11, "bold"),width=24, height=1, command=self.connect_drone)
        self.btn_connect.pack(pady=5)

        self.btn_close = tk.Button(root, text="Disconnect", bg="#c62828", fg="white", font=("Arial", 11, "bold"),width=24, height=1, state=tk.DISABLED, command=self.close_connection)
        self.btn_close.pack(pady=5)

        self.lbl_status = tk.Label(root, text="Status: Disconnected", fg="#ff5252", bg="#2b2b2b",font=("Arial", 11, "bold"))
        self.lbl_status.pack(pady=10)

        self.btn_arm = tk.Button(root, text="ARM MOTORS", bg="#f57c00", fg="white", font=("Arial", 11, "bold"),width=24, height=2, state=tk.DISABLED, command=self.arm_drone)
        self.btn_arm.pack(pady=10)

        tk.Label(root, text="Flight Modes:", bg="#2b2b2b", fg="#cccccc", font=("Arial", 11, "bold")).pack(pady=5)

        modes = ["GUIDED", "STABILIZE", "LOITER", "LAND", "RTL"]
        for mode in modes:
            b = tk.Button(root, text=mode, bg="#37474f", fg="white", font=("Arial", 10, "bold"), width=22, height=1,state=tk.DISABLED, command=lambda m=mode: self.set_mode(m))
            b.pack(pady=3)
            self.mode_buttons.append(b)

    def connect_drone(self):
        conn_str = self.entry_conn.get()
        try:
            self.lbl_status.config(text="Status: Connecting...", fg="#ffa726")
            self.root.update()

            self.master = mavutil.mavlink_connection(conn_str)
            self.master.wait_heartbeat(timeout=3)

            self.lbl_status.config(text="Status: Connected", fg="#66bb6a")
            self.btn_connect.config(state=tk.DISABLED)
            self.btn_close.config(state=tk.NORMAL)
            self.btn_arm.config(state=tk.NORMAL)
            for b in self.mode_buttons:
                b.config(state=tk.NORMAL)

            messagebox.showinfo("Success", "Successfully connected to MAVLink device!")
        except Exception as e:
            self.lbl_status.config(text="Status: Connection Failed", fg="#ff5252")
            messagebox.showerror("Error", f"Could not connect:\n{e}")

    def close_connection(self):
        if self.master:
            self.master.close()
            self.master = None

        self.lbl_status.config(text="Status: Disconnected", fg="#ff5252")
        self.btn_connect.config(state=tk.NORMAL)
        self.btn_close.config(state=tk.DISABLED)
        self.btn_arm.config(state=tk.DISABLED)
        for b in self.mode_buttons:
            b.config(state=tk.DISABLED)

    def arm_drone(self):
        if self.master:
            self.master.arducopter_arm()
            self.lbl_status.config(text="Status: Arm Command Sent", fg="#29b6f6")

    def set_mode(self, mode_name):
        if self.master:
            mode_map = self.master.mode_mapping()
            if mode_name in mode_map:
                mode_id = mode_map[mode_name]
                self.master.set_mode(mode_id)
                self.lbl_status.config(text=f"Status: Mode -> {mode_name}", fg="#29b6f6")

    def on_closing(self):
        if self.master:
            try:
                self.master.close()
            except:
                pass
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = DroneGCSApp(root)
    root.mainloop()