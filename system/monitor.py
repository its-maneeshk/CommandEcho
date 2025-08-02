import psutil

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_ram_usage():
    return psutil.virtual_memory().percent

def get_disk_usage():
    return psutil.disk_usage('/').percent

def system_status(verbose=False):
    cpu = get_cpu_usage()
    ram = get_ram_usage()
    disk = get_disk_usage()

    if verbose:
        return (
            f"🧠 System Diagnostics:\n"
            f"• CPU Usage: {cpu}%\n"
            f"• RAM Usage: {ram}%\n"
            f"• Disk Usage: {disk}%"
        )

    alerts = []
    if cpu > 85:
        alerts.append(f"⚠️ High CPU usage: {cpu}%")
    if ram > 85:
        alerts.append(f"⚠️ High RAM usage: {ram}%")
    if disk > 90:
        alerts.append(f"⚠️ Low disk space: {disk}% used")

    if alerts:
        return " ".join(alerts)
    return "✅ All systems are running smoothly."
