
from logger import logger_mongo

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
