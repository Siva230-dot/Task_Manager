import psutil

def get_process_info():
    print(f"{'PID':>6} | {'Process Name':<30} | {'CPU%':>6} | {'Memory(MB)':>10} | User")
    print("-" * 80)
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'username']):
        try:
            name = proc.info['name'] or "Unknown"
            pid = proc.info['pid']
            cpu = proc.cpu_percent(interval=0.1)
            mem = proc.info['memory_info'].rss / (1024 * 1024)  # MB
            user = proc.info['username'] or "System"
            print(f"{pid:>6} | {name:<30.30} | {cpu:6.2f} | {mem:10.2f} | {user}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

if __name__ == "__main__":
    get_process_info()
