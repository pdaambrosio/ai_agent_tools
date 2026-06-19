from os import name

from langchain_core.tools import tool
from datetime import datetime
import platform
import psutil
import json


@tool
def check_cpu() -> str:
    """
    Check CPU usage in percent.
    Return usage per core and general average.
    """
    cpu_usage: float = psutil.cpu_percent(interval=1)
    cpu_usage_per_core: float = psutil.cpu_percent(percpu=True)

    result: dict = {
        "cpu_usage": f"{cpu_usage:.2f}%",
        "cpu_usage_per_core": [f"Core {i}: {use}%" for i, use in enumerate(cpu_usage_per_core)],
        "cpu_count": psutil.cpu_count(),
        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }
    return json.dumps(result, indent=2, ensure_ascii=False)


@tool
def check_memory() -> str:
    """
    Check system memory usage.
    Return system memory total, usage, free and percent.
    """
    memory = psutil.virtual_memory()
    total_gb: float = round(memory.total / (1024**3), 2)
    used_gb: float = round(memory.used / (1024**3), 2)
    free_gb: float = round(memory.free / (1024**3), 2)
    available_gb: float = round(memory.available / (1024**3), 2)
    percent: float = round(memory.percent, 2)

    result: dict = {
        "total_gb": f"{total_gb:.2f}GB",
        "used_gb": f"{used_gb:.2f}GB",
        "free_gb": f"{free_gb:.2f}GB",
        "available_gb": f"{available_gb:.2f}GB",
        "percent": f"{percent:.2f}%",
        "alert": "⚠️ CRÍTICO" if percent > 80 else "✅ Normal",
        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }
    return json.dumps(result, indent=2, ensure_ascii=False)


@tool
def check_disk() -> str:
    """
    Check disk usage.
    Return disk usage total, usage, free and percent.
    """
    disk_usage = psutil.disk_usage('/')
    total_gb: float = round(disk_usage.total / (1024**3), 2)
    used_gb: float = round(disk_usage.used / (1024**3), 2)
    free_gb: float = round(disk_usage.free / (1024**3), 2)
    percent: float = round(disk_usage.percent, 2)

    result: dict = {
        "total_gb": f"{total_gb:.2f}GB",
        "used_gb": f"{used_gb:.2f}GB",
        "free_gb": f"{free_gb:.2f}GB",
        "percent": f"{percent:.2f}%",
        "alert": "⚠️ CRÍTICO" if percent > 80 else "✅ Normal",
        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }

    return json.dumps(result, indent=2, ensure_ascii=False)


@tool
def list_top_five_process():
    """
    List the five processes that consume the most memory.
    Useful to identify memory leaks
    """
    processes: list = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            processes.append({
                "pid": proc.info['pid'],
                "name": proc.info['name'],
                "memory_percent": round(proc.info['memory_percent'], 2),
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    top_five_per_memory: list = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:5]

    result: dict = {
        "top_five_per_memory": top_five_per_memory,
        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }

    return json.dumps(result, indent=2, ensure_ascii=False)


@tool
def system_information():
    """
    Get general system information.
    Return SO, hostname, uptime, etc.
    """
    uptime_seconds: float = datetime.now().timestamp() - psutil.boot_time()
    uptime_hours: float = round(uptime_seconds / 3600, 2)
    so: str = platform.system()
    version: str = platform.release()
    hostname: str = platform.node()
    architecture: str = platform.machine()

    result: dict = {
        "so": so,
        "version": version,
        "hostname": hostname,
        "architecture": architecture,
        "uptime_hours": uptime_hours,
        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }

    return json.dumps(result, indent=2, ensure_ascii=False)

