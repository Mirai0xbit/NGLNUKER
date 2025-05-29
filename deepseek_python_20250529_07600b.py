import requests
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from queue import Queue

# Simulated reporting function (replace with actual platform APIs)
def report_account(platform, account_url, proxy=None):
    try:
        # Simulate API request with proxy
        proxies = {"http": proxy, "https": proxy} if proxy else None
        
        # This would be replaced with actual platform API calls
        print(f"Reporting {account_url} on {platform} using proxy: {proxy}")
        time.sleep(random.uniform(1, 3))  # Simulate request delay
        
        # Simulate success/failure
        return random.choice([True, False])
    except Exception as e:
        return False

class ReportingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Account Reporting Tool")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Platform selection
        ttk.Label(root, text="Platform:").pack(pady=5)
        self.platform = ttk.Combobox(root, values=["Instagram", "Facebook", "TikTok"])
        self.platform.pack(fill=tk.X, padx=50, pady=5)
        self.platform.set("Instagram")
        
        # Account URL
        ttk.Label(root, text="Account URL:").pack(pady=5)
        self.account_url = ttk.Entry(root)
        self.account_url.pack(fill=tk.X, padx=50, pady=5)
        
        # Report count
        ttk.Label(root, text="Report Count:").pack(pady=5)
        self.report_count = ttk.Spinbox(root, from_=1, to=100)
        self.report_count.pack(fill=tk.X, padx=50, pady=5)
        self.report_count.set(5)
        
        # Proxy list
        ttk.Label(root, text="Proxies (one per line):").pack(pady=5)
        self.proxy_text = tk.Text(root, height=5)
        self.proxy_text.pack(fill=tk.X, padx=50, pady=5)
        
        # Log console
        ttk.Label(root, text="Logs:").pack(pady=5)
        self.log_console = tk.Text(root, height=10, state=tk.DISABLED)
        self.log_console.pack(fill=tk.BOTH, padx=50, pady=5, expand=True)
        
        # Progress bar
        self.progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=500, mode='determinate')
        self.progress.pack(pady=10)
        
        # Start button
        self.start_btn = ttk.Button(root, text="Start Reporting", command=self.start_reporting)
        self.start_btn.pack(pady=10)
        
        # Reporting queue
        self.queue = Queue()
        self.running = False
        self.success_count = 0
        self.fail_count = 0

    def log_message(self, message):
        self.log_console.config(state=tk.NORMAL)
        self.log_console.insert(tk.END, message + "\n")
        self.log_console.see(tk.END)
        self.log_console.config(state=tk.DISABLED)

    def worker(self):
        while self.running:
            platform, url, proxy = self.queue.get()
            if platform and url:
                success = report_account(platform, url, proxy)
                if success:
                    self.success_count += 1
                    self.log_message(f"[SUCCESS] Reported {url}")
                else:
                    self.fail_count += 1
                    self.log_message(f"[FAILED] Could not report {url}")
                
                # Update progress
                self.progress['value'] = ((self.success_count + self.fail_count) / 
                                        int(self.report_count.get())) * 100
            self.queue.task_done()

    def start_reporting(self):
        if self.running:
            return
            
        # Validate inputs
        account_url = self.account_url.get()
        if not account_url.startswith(("http://", "https://")):
            messagebox.showerror("Error", "Invalid URL format")
            return
        
        # Get proxies
        proxies = self.proxy_text.get("1.0", tk.END).strip().splitlines()
        if not proxies:
            messagebox.showwarning("Warning", "No proxies provided!")
        
        # Reset counters
        self.success_count = 0
        self.fail_count = 0
        self.progress['value'] = 0
        self.log_message("=== Starting reporting process ===")
        
        # Setup queue
        for _ in range(int(self.report_count.get())):
            proxy = random.choice(proxies) if proxies else None
            self.queue.put((self.platform.get(), account_url, proxy))
        
        # Start workers
        self.running = True
        for _ in range(3):  # 3 worker threads
            threading.Thread(target=self.worker, daemon=True).start()
        
        # Check completion
        threading.Thread(target=self.check_completion, daemon=True).start()

    def check_completion(self):
        self.queue.join()
        self.running = False
        self.log_message(f"\nCompleted: {self.success_count} successful, {self.fail_count} failed")
        self.progress['value'] = 100

if __name__ == "__main__":
    root = tk.Tk()
    app = ReportingApp(root)
    root.mainloop()