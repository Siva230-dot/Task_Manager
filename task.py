import psutil
import time
import win32gui
import win32process

def get_visible_windows_pids():
    """Return a set of PIDs for visible apps."""
    def callback(hwnd, pid_list):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            pid_list.add(pid)
    pids = set()
    win32gui.EnumWindows(callback, pids)
    return pids

def get_running_apps():
    visible_pids = get_visible_windows_pids()
    process_data = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'username']):
        try:
            if proc.info['pid'] in visible_pids:
                name = proc.info['name']
                pid = proc.info['pid']
                cpu = proc.cpu_percent(interval=None)
                mem = proc.info['memory_info'].rss / (1024 * 1024)
                user = proc.info['username']
                process_data.append((pid, name, cpu, mem, user))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return process_data

def display_apps():
    header = f"{'PID':>6} | {'App Name':<30} | {'CPU%':>6} | {'Memory(MB)':>10} | User"
    print(header)
    print("-" * 80)
    line_count = 0

    while True:
        processes = sorted(get_running_apps(), key=lambda x: x[2], reverse=True)
        for pid, name, cpu, mem, user in processes:
            print(f"{pid:>6} | {name:<30.30} | {cpu:6.2f} | {mem:10.2f} | {user}")
        print("-" * 80)
        print("Refreshing...\n")

        # Move cursor up to overwrite previous lines instead of clearing
        total_lines = len(processes) + 4
        print(f"\033[{total_lines}A", end="")  # ANSI cursor move-up escape sequence
        time.sleep(1.5)

if __name__ == "__main__":
    display_apps()
