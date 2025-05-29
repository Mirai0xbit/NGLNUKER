import tkinter as tk
from tkinter import ttk, messagebox
from time import sleep

class FacebookReportBotDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Facebook Report Bot (DEMO)")
        self.root.geometry("500x400")
        
        # Warning Label
        warning_label = ttk.Label(
            root,
            text="⚠️ WARNING: Mass reporting is against Facebook's TOS. This is a DEMO only.",
            foreground="red",
            font=("Arial", 10, "bold"),
            wraplength=400,
            justify="center"
        )
        warning_label.pack(pady=10)
        
        # Login Frame
        login_frame = ttk.LabelFrame(root, text="Facebook Login (Simulated)")
        login_frame.pack(pady=10, padx=20, fill="x")
        
        ttk.Label(login_frame, text="Email:").grid(row=0, column=0, padx=5, pady=5)
        self.email_entry = ttk.Entry(login_frame, width=30)
        self.email_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(login_frame, show="*", width=30)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Report Frame
        report_frame = ttk.LabelFrame(root, text="Report Profile (Simulated)")
        report_frame.pack(pady=10, padx=20, fill="x")
        
        ttk.Label(report_frame, text="Profile URL:").grid(row=0, column=0, padx=5, pady=5)
        self.url_entry = ttk.Entry(report_frame, width=30)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(report_frame, text="Reason:").grid(row=1, column=0, padx=5, pady=5)
        self.reason_combo = ttk.Combobox(
            report_frame,
            values=[
                "Pretending to be someone",
                "Harassment",
                "Hate speech",
                "Spam",
                "Fake account"
            ],
            width=27
        )
        self.reason_combo.grid(row=1, column=1, padx=5, pady=5)
        self.reason_combo.current(0)
        
        # Buttons
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10)
        
        self.login_button = ttk.Button(
            button_frame,
            text="Simulate Login",
            command=self.simulate_login
        )
        self.login_button.pack(side="left", padx=5)
        
        self.report_button = ttk.Button(
            button_frame,
            text="Simulate Report",
            command=self.simulate_report,
            state="disabled"
        )
        self.report_button.pack(side="left", padx=5)
        
        # Logs
        self.log_text = tk.Text(root, height=8, state="disabled")
        self.log_text.pack(pady=10, padx=20, fill="x")
        
    def simulate_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Email and password are required!")
            return
        
        self.log("Attempting simulated login...")
        sleep(2)  # Simulate delay
        self.log(f"Logged in as: {email} (SIMULATED)")
        self.report_button["state"] = "normal"
        
    def simulate_report(self):
        url = self.url_entry.get()
        reason = self.reason_combo.get()
        
        if not url:
            messagebox.showerror("Error", "Profile URL is required!")
            return
        
        self.log(f"Reporting {url} for: {reason}...")
        sleep(2)  # Simulate delay
        self.log("Report submitted (SIMULATED)")
        messagebox.showinfo(
            "Demo Only",
            "This is a simulation. No real reports were sent.\n\n"
            "Mass reporting is against Facebook's policies."
        )
        
    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = FacebookReportBotDemo(root)
    root.mainloop()
