from fastapi import FastAPI
import psutil

app = FastAPI()
import logging
from typing import Dict, Any, Optional
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

##########################################
# Configure logging.
##########################################
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger('mongodb_operations')


##########################################
# Configure Mongo.
##########################################
class MongoDBHandler:
    def __init__(self, connection_url: str):
        """
        Initialize MongoDB handler with connection URL
        
        Args:
            connection_url (str): MongoDB connection URL
        """
        self.connection_url = connection_url
        self.client = None
        logger.info("MongoDB handler initialized")

    def connect(self) -> bool:
        """
        Establish connection to MongoDB
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.client = MongoClient(self.connection_url)
            # Ping the server to verify connection
            self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
            return True
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during connection: {str(e)}")
            return False

    def disconnect(self) -> None:
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            self.client = None
            logger.info("Disconnected from MongoDB")
        else:
            logger.warning("No active connection to disconnect")

    def write_doc(self, database: str, collection: str, document: Dict[str, Any]) -> Optional[str]:
        """
        Write a document to MongoDB
        
        Args:
            database (str): Database name
            collection (str): Collection name
            document (Dict): Document to insert
            
        Returns:
            Optional[str]: Document ID if successful, None otherwise
        """
        if not self.client:
            logger.error("No active connection. Call connect() first")
            return None

        try:
            db = self.client[database]
            coll = db[collection]
            result = coll.insert_one(document)
            doc_id = str(result.inserted_id)
            logger.info(f"Successfully inserted document with ID: {doc_id}")
            return doc_id
        except OperationFailure as e:
            logger.error(f"Failed to write document: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during write: {str(e)}")
            return None

    def read_docs(self, database: str, collection: str, query: Dict[str, Any] = None) -> list:
        """
        Read documents from MongoDB
        
        Args:
            database (str): Database name
            collection (str): Collection name
            query (Dict): Query filter (optional)
            
        Returns:
            list: List of documents
        """
        if not self.client:
            logger.error("No active connection. Call connect() first")
            return []

        try:
            db = self.client[database]
            coll = db[collection]
            query = query or {}
            documents = list(coll.find(query))
            
            logger.info(f"Retrieved {len(documents)} documents")
            
            # Print documents to stdout
            print("\n=== Retrieved Documents ===")
            for doc in documents:
                print(f"Document ID: {doc['_id']}")
                print(doc)
                print("------------------------")
            
            return documents
        except OperationFailure as e:
            logger.error(f"Failed to read documents: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error during read: {str(e)}")
            return []

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

@app.get("/readiness")
async def readiness_probe():
    return {"message": "Hello health-check readiness_probe!"}

@app.get("/liveness")
async def liveness_probe():
    return {"message": "Hello health-check liveness_probe!"}



##########################################
# Configure User.
##########################################

@app.get("/get_users_info")
async def startup_probe():
    return {"message": "Hello health-check get_users_info!"}

@app.get("/set_user_info")
async def readiness_probe():
    return {"message": "Hello health-check set_user_info!"}

@app.get("/check_redis")
async def liveness_probe():
    return {"message": "Hello health-check check_redis!"}

from fastapi import FastAPI, HTTPException, status
from typing import Dict, Any
from datetime import datetime

app = FastAPI()

@app.get("/check_mongo", response_model=Dict[str, Any])
async def check_mongo():
    try:
        mongo_connection_url = "mongodb://root:u3mmjey8rl@localhost:27017"
        mongo_db_name = "dev"
        mongo_co_name = "users"
        mongo_handler = MongoDBHandler(mongo_connection_url)
        
        if not mongo_handler.connect():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail={
                    "message": "MongoDB connection failed",
                    "timestamp": datetime.utcnow().isoformat(),
                    "service": "mongodb"
                }
            )

        # Write example
        doc = {
            "name": "NarkisAtGolash",
            "age": "120",
            "page": "NarkisAtGolash@example.com",
            "telegram": "NarkisAtGolash@example.com",
            "email": "NarkisAtGolash@example.com"
        }
        
        doc_id = mongo_handler.write_doc(mongo_db_name, mongo_co_name, doc)
        if not doc_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "message": "Failed to write document to MongoDB",
                    "timestamp": datetime.utcnow().isoformat(),
                    "service": "mongodb"
                }
            )

        # Read example
        documents = mongo_handler.read_docs(mongo_db_name, mongo_co_name, {"name": "NarkisAtGolash"})
        if not documents:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "No documents found",
                    "timestamp": datetime.timezone-aware().isoformat(),
                    "service": "mongodb"
                }
            )

        # Cleanup
        mongo_handler.disconnect()

        # Success response
        return {
            "status": "healthy",
            "message": "MongoDB health check passed",
            "timestamp": datetime.timezone-aware().isoformat(),
            "service": "mongodb",
            "details": {
                "connection": "successful",
                "write_test": "passed",
                "read_test": "passed",
                "documents_found": len(documents)
            }
        }

    except HTTPException:
        raise  # Re-raise FastAPI HTTP exceptions
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": f"Unexpected error during MongoDB health check: {str(e)}",
                "timestamp": datetime.utcnow().isoformat(),
                "service": "mongodb",
                "error_type": type(e).__name__
            }
        )

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

