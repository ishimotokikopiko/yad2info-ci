from typing import Dict, Any, Optional
from datetime import datetime
import psutil
from fastapi import FastAPI HTTPException, status
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
#import ng_utils.logger
app = FastAPI()




##########################################
# Configure Health.
##########################################

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

@app.get("/")
async def startup_probe():
    return {"message": "Hello health-check startup_probe!"}

@app.get("/liveness")
async def liveness_probe():
    return {"message": "Hello health-check liveness_probe!"}



##########################################
# Configure User.
##########################################

# @app.get("/get_users_info")
# async def startup_probe():
#     return {"message": "Hello health-check get_users_info!"}

# @app.get("/set_user_info")
# async def readiness_probe():
#     return {"message": "Hello health-check set_user_info!"}

# @app.get("/check_redis")
# async def liveness_probe():
#     return {"message": "Hello health-check check_redis!"}


# @app.get("/check_mongo", response_model=Dict[str, Any])
# async def check_mongo():
#     try:
#         mongo_connection_url = "mongodb://root:u3mmjey8rl@localhost:27017"
#         mongo_db_name = "dev"
#         mongo_co_name = "users"
#         mongo_handler = MongoDBHandler(mongo_connection_url)
        
#         if not mongo_handler.connect():
#             raise HTTPException(
#                 status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
#                 detail={
#                     "message": "MongoDB connection failed",
#                     "timestamp": datetime.utcnow().isoformat(),
#                     "service": "mongodb"
#                 }
#             )

#         # Write example
#         doc = {
#             "name": "NarkisAtGolash",
#             "age": "120",
#             "page": "NarkisAtGolash@example.com",
#             "telegram": "NarkisAtGolash@example.com",
#             "email": "NarkisAtGolash@example.com"
#         }
        
#         doc_id = mongo_handler.write_doc(mongo_db_name, mongo_co_name, doc)
#         if not doc_id:
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail={
#                     "message": "Failed to write document to MongoDB",
#                     "timestamp": datetime.utcnow().isoformat(),
#                     "service": "mongodb"
#                 }
#             )

#         # Read example
#         documents = mongo_handler.read_docs(mongo_db_name, mongo_co_name, {"name": "NarkisAtGolash"})
#         if not documents:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail={
#                     "message": "No documents found",
#                     "timestamp": datetime.timezone-aware().isoformat(),
#                     "service": "mongodb"
#                 }
#             )

#         # Cleanup
#         mongo_handler.disconnect()

#         # Success response
#         return {
#             "status": "healthy",
#             "message": "MongoDB health check passed",
#             "timestamp": datetime.timezone-aware().isoformat(),
#             "service": "mongodb",
#             "details": {
#                 "connection": "successful",
#                 "write_test": "passed",
#                 "read_test": "passed",
#                 "documents_found": len(documents)
#             }
#         }

#     except HTTPException:
#         raise  # Re-raise FastAPI HTTP exceptions
#     except Exception as e:
#         # Handle unexpected errors
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail={
#                 "message": f"Unexpected error during MongoDB health check: {str(e)}",
#                 "timestamp": datetime.utcnow().isoformat(),
#                 "service": "mongodb",
#                 "error_type": type(e).__name__
#             }
#         )

@app.get("/check_health")
async def get_health_check(cpu_threshold: int = 80, ram_threshold: int = 80, disk_threshold: int = 80):
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

