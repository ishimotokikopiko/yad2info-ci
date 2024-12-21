from fastapi import FastAPI
import psutil

app = FastAPI()

def health_check(cpu_threshold: int, ram_threshold: int, disk_threshold: int) -> dict:
    """
    Perform a health check on the system and return status with actual metrics.

    Args:
        cpu_threshold (int): Maximum allowed CPU usage percentage.
        ram_threshold (int): Maximum allowed RAM usage percentage.
        disk_threshold (int): Maximum allowed Disk usage percentage.

    Returns:
        dict: Health check result with status and actual metrics.
    """
    
    # Get system usage stats
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    # Determine health status
    status = "PASS"
    if cpu_usage > cpu_threshold or ram_usage > ram_threshold or disk_usage > disk_threshold:
        status = "FAIL"

    return {
        "status": status,
        "metrics": {
            "cpu_usage": cpu_usage,
            "ram_usage": ram_usage,
            "disk_usage": disk_usage
        },
        "thresholds": {
            "cpu_threshold": cpu_threshold,
            "ram_threshold": ram_threshold,
            "disk_threshold": disk_threshold
        }
    }

@app.get("/health_check")
def get_health_check(cpu_threshold: int = 80, ram_threshold: int = 80, disk_threshold: int = 80):
    """
    Health check endpoint.

    Args:
        cpu_threshold (int): CPU usage threshold in percentage (default 80).
        ram_threshold (int): RAM usage threshold in percentage (default 80).
        disk_threshold (int): Disk usage threshold in percentage (default 80).

    Returns:
        dict: Health check result including status, actual metrics, and thresholds.
    """
    return health_check(cpu_threshold, ram_threshold, disk_threshold)

@app.get("/")
def read_root():
    return {"message": "Hello health_check!"}

