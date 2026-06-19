from os import name

from langchain_core.tools import tool
from datetime import datetime
import psutil
import json

import main


@tool
def check_cpu() -> str:
    """
    Check CPU usage in percent.
    Return usage per core and general average.
    """
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_usage_per_core = psutil.cpu_percent(percpu=True)

    result = {
        "cpu_usage": f"{cpu_usage:.2f}%",
        "cpu_usage_per_core": [f"Core {i}: {use}%" for i, use in enumerate(cpu_usage_per_core)],
        "cpu_count": psutil.cpu_count(),
        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }
    return json.dumps(result, indent=2, ensure_ascii=False)
