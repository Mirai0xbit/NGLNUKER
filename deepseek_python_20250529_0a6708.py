import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
import random
import threading
import json
import os
from fake_useragent import UserAgent

class MassReportBot:
    def __init__(self, root):
        self.root = root
        self.root.title("Mass Report Bot (Educational)")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Variables
        self.platform = tk.StringVar(value="instagram")
        self.report_reason = tk.StringVar(value="spam")
        self.targets = []
        self.proxies = []
        self.running = False
        self.reports_made = 0
        self.delay = tk.IntVar(value=5)
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        # Platform Selection
        platform_frame = ttk.LabelFrame(self.root, text="Platform", padding=10)
        platform_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Radiobutton(platform_frame, text="Instagram", variable=self.platform, value="instagram").pack(side="left", padx=5)
        ttk.Radiobutton(platform_frame, text="Facebook", variable=self.platform, value="facebook").pack(side="left", padx=5)
        ttk.Radiobutton(platform_frame, text="TikTok", variable=self.platform, value="tiktok").pack(side="left", padx=5)
        
        # Report Reason
        reason_frame = ttk.LabelFrame(self.root, text="Report Reason", padding=10)
        reason_frame.pack(fill="x", padx=10, pady=5)
        
        reasons = {
            "instagram": ["spam", "nudity", "violence", "hate speech", "harassment"],
            "facebook": ["spam", "nudity", "violence", "false information", "hate speech"],
            "tiktok": ["spam", "nudity", "harassment", "dangerous acts", "hate speech"]
        }
        
        self.reason_menu = ttk.Combobox(reason_frame, textvariable=self.report_reason, values=reasons["instagram"])
        self.reason_menu.pack(fill="x")
        
        # Update reasons when platform changes
        self.platform.trace_add("write", lambda *args: self.update_reasons())
        
        # Targets
        target_frame = ttk.LabelFrame(self.root, text="Targets", padding=10)
        target_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.target_listbox = tk.Listbox(target_frame)
        self.target_listbox.pack(fill="both", expand=True)
        
        target_button_frame = ttk.Frame(target_frame)
        target_button_frame.pack(fill="x", pady=5)
        
        ttk.Button(target_button_frame, text="Add Target", command=self.add_target).pack(side="left", padx=5)
        ttk.Button(target_button_frame, text="Import Targets", command=self.import_targets).pack(side="left", padx=5)
        ttk.Button(target_button_frame, text="Clear Targets", command=self.clear_targets).pack(side="left", padx=5)
        
        # Proxies
        proxy_frame = ttk.LabelFrame(self.root, text="Proxies", padding=10)
        proxy_frame.pack(fill="x", padx=10, pady=5)
        
        self.proxy_listbox = tk.Listbox(proxy_frame, height=4)
        self.proxy_listbox.pack(fill="x")
        
        proxy_button_frame = ttk.Frame(proxy_frame)
        proxy_button_frame.pack(fill="x", pady=5)
        
        ttk.Button(proxy_button_frame, text="Add Proxy", command=self.add_proxy).pack(side="left", padx=5)
        ttk.Button(proxy_button_frame, text="Import Proxies", command=self.import_proxies).pack(side="left", padx=5)
        ttk.Button(proxy_button_frame, text="Clear Proxies", command=self.clear_proxies).pack(side="left", padx=5)
        
        # Settings
        settings_frame = ttk.LabelFrame(self.root, text="Settings", padding=10)
        settings_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(settings_frame, text="Delay (seconds):").pack(side="left")
        ttk.Spinbox(settings_frame, from_=1, to=60, textvariable=self.delay).pack(side="left", padx=5)
        
        # Status
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill="x", padx=10, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Ready", foreground="green")
        self.status_label.pack(side="left")
        
        self.report_count_label = ttk.Label(status_frame, text="Reports made: 0")
        self.report_count_label.pack(side="right")
        
        # Control Buttons
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill="x", padx=10, pady=5)
        
        self.start_button = ttk.Button(control_frame, text="Start Reporting", command=self.start_reporting)
        self.start_button.pack(side="left", padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="Stop Reporting", command=self.stop_reporting, state="disabled")
        self.stop_button.pack(side="left", padx=5)
        
        # Save/Load Config
        config_frame = ttk.Frame(self.root)
        config_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(config_frame, text="Save Config", command=self.save_config).pack(side="left", padx=5)
        ttk.Button(config_frame, text="Load Config", command=self.load_config).pack(side="left", padx=5)
        
    def update_reasons(self):
        platform = self.platform.get()
        reasons = {
            "instagram": ["spam", "nudity", "violence", "hate speech", "harassment"],
            "facebook": ["spam", "nudity", "violence", "false information", "hate speech"],
            "tiktok": ["spam", "nudity", "harassment", "dangerous acts", "hate speech"]
        }
        self.reason_menu["values"] = reasons.get(platform, ["spam"])
        self.report_reason.set("spam")
        
    def add_target(self):
        target = simpledialog.askstring("Add Target", "Enter target URL or username:")
        if target:
            self.targets.append(target)
            self.target_listbox.insert(tk.END, target)
            
    def import_targets(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r") as f:
                    targets = [line.strip() for line in f.readlines() if line.strip()]
                    self.targets.extend(targets)
                    self.target_listbox.delete(0, tk.END)
                    for target in self.targets:
                        self.target_listbox.insert(tk.END, target)
                messagebox.showinfo("Success", f"Imported {len(targets)} targets")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import targets: {str(e)}")
                
    def clear_targets(self):
        self.targets = []
        self.target_listbox.delete(0, tk.END)
        
    def add_proxy(self):
        proxy = simpledialog.askstring("Add Proxy", "Enter proxy (format: ip:port:user:pass or ip:port):")
        if proxy:
            self.proxies.append(proxy)
            self.proxy_listbox.insert(tk.END, proxy)
            
    def import_proxies(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r") as f:
                    proxies = [line.strip() for line in f.readlines() if line.strip()]
                    self.proxies.extend(proxies)
                    self.proxy_listbox.delete(0, tk.END)
                    for proxy in self.proxies:
                        self.proxy_listbox.insert(tk.END, proxy)
                messagebox.showinfo("Success", f"Imported {len(proxies)} proxies")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import proxies: {str(e)}")
                
    def clear_proxies(self):
        self.proxies = []
        self.proxy_listbox.delete(0, tk.END)
        
    def save_config(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            config = {
                "platform": self.platform.get(),
                "report_reason": self.report_reason.get(),
                "targets": self.targets,
                "proxies": self.proxies,
                "delay": self.delay.get()
            }
            try:
                with open(file_path, "w") as f:
                    json.dump(config, f)
                messagebox.showinfo("Success", "Configuration saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save config: {str(e)}")
                
    def load_config(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r") as f:
                    config = json.load(f)
                
                self.platform.set(config.get("platform", "instagram"))
                self.report_reason.set(config.get("report_reason", "spam"))
                self.delay.set(config.get("delay", 5))
                
                self.targets = config.get("targets", [])
                self.target_listbox.delete(0, tk.END)
                for target in self.targets:
                    self.target_listbox.insert(tk.END, target)
                
                self.proxies = config.get("proxies", [])
                self.proxy_listbox.delete(0, tk.END)
                for proxy in self.proxies:
                    self.proxy_listbox.insert(tk.END, proxy)
                
                messagebox.showinfo("Success", "Configuration loaded successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load config: {str(e)}")
                
    def start_reporting(self):
        if not self.targets:
            messagebox.showwarning("Warning", "No targets specified")
            return
            
        self.running = True
        self.reports_made = 0
        self.start_button["state"] = "disabled"
        self.stop_button["state"] = "normal"
        self.status_label.config(text="Running...", foreground="blue")
        
        # Start reporting in a separate thread
        threading.Thread(target=self.report_worker, daemon=True).start()
        
    def stop_reporting(self):
        self.running = False
        self.start_button["state"] = "normal"
        self.stop_button["state"] = "disabled"
        self.status_label.config(text="Stopped", foreground="red")
        
    def report_worker(self):
        ua = UserAgent()
        
        for target in self.targets:
            if not self.running:
                break
                
            try:
                # Simulate reporting (in a real tool, this would make actual API calls)
                proxy = random.choice(self.proxies) if self.proxies else None
                user_agent = ua.random
                
                # Simulate report
                time.sleep(self.delay.get())
                self.reports_made += 1
                
                # Update UI
                self.root.after(0, self.update_status, target)
                
            except Exception as e:
                self.root.after(0, self.show_error, f"Error reporting {target}: {str(e)}")
                
        self.root.after(0, self.stop_reporting)
        
    def update_status(self, target):
        self.report_count_label.config(text=f"Reports made: {self.reports_made}")
        self.status_label.config(text=f"Reported {target}", foreground="green")
        
    def show_error(self, message):
        messagebox.showerror("Error", message)

if __name__ == "__main__":
    from tkinter import simpledialog
    
    root = tk.Tk()
    app = MassReportBot(root)
    root.mainloop()