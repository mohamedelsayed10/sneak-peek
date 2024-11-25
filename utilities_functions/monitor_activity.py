# monitor_activity.py

import time
import pygetwindow as gw
import pyperclip
import openpyxl


# Select the active worksheet or a specific sheet

class ActivityMonitor:
    def __init__(self):
        self.active_window = None
        self.last_copied = ""

    def get_active_window_title(self):
        """Get the title of the currently active window."""
        try:
            return gw.getActiveWindow().title
        except Exception:
            return None

    def check_copy_paste(self):
        """Check if the clipboard content has changed."""
        current_copied = pyperclip.paste()
        if current_copied != self.last_copied:
            print("Copy-Paste detected!")
            self.last_copied = current_copied

    def monitor(self,actvity_flag,user_id, exam_id,workbook,workbook_path):
        """Monitor for active window changes and copy-paste actions."""
        while True:
            time.sleep(1)  # Check every second
            current_active_window = self.get_active_window_title()

            if current_active_window != self.active_window:
                new_row = [f"Window changed to: {current_active_window}", time.strftime("%Y-%m-%d %H:%M:%S"),user_id,exam_id]  # Replace with your data
                sheet=workbook.active
                sheet.append(new_row)
                workbook.save(workbook_path)
                print(f"Window changed to: {current_active_window}")
                self.active_window = current_active_window
            
            self.check_copy_paste()
            if actvity_flag[0]== False:
                break
    

def start_monitoring_activity(actvity_flag,user_id, exam_id,workbook,workbook_path):
    monitor = ActivityMonitor()
    monitor.monitor(actvity_flag,user_id, exam_id,workbook,workbook_path)
