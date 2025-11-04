"""
AWS integration utilities
"""
import boto3
from botocore.exceptions import ClientError
from pathlib import Path
from config import AWS_CONFIG
from src.utils.logger import get_logger

logger = get_logger(__name__)

class AWSManager:
    """AWS services manager"""
    
    def __init__(self):
        self.s3_client = None
        self.s3_resource = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize AWS clients"""
        try:
            if AWS_CONFIG["access_key_id"]:
                self.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=AWS_CONFIG["access_key_id"],
                    aws_secret_access_key=AWS_CONFIG["secret_access_key"],
                    region_name=AWS_CONFIG["region"]
                )
                self.s3_resource = boto3.resource(
                    's3',
                    aws_access_key_id=AWS_CONFIG["access_key_id"],
                    aws_secret_access_key=AWS_CONFIG["secret_access_key"],
                    region_name=AWS_CONFIG["region"]
                )
                logger.info("AWS clients initialized")
            else:
                logger.warning("AWS credentials not configured")
        except Exception as e:
            logger.error(f"AWS client initialization failed: {e}")
    
    def upload_model(self, local_path: str, s3_key: str = None):
        """Upload model to S3"""
        if not self.s3_client:
            logger.warning("AWS S3 client not available")
            return False
        
        try:
            if not s3_key:
                s3_key = f"{AWS_CONFIG['s3_model_path']}{Path(local_path).name}"
            
            self.s3_client.upload_file(
                local_path,
                AWS_CONFIG["s3_bucket"],
                s3_key
            )
            logger.info(f"Model uploaded to s3://{AWS_CONFIG['s3_bucket']}/{s3_key}")
            return True
        except ClientError as e:
            logger.error(f"Model upload failed: {e}")
            return False
    
    def download_model(self, s3_key: str, local_path: str):
        """Download model from S3"""
        if not self.s3_client:
            logger.warning("AWS S3 client not available")
            return False
        
        try:
            self.s3_client.download_file(
                AWS_CONFIG["s3_bucket"],
                s3_key,
                local_path
            )
            logger.info(f"Model downloaded from s3://{AWS_CONFIG['s3_bucket']}/{s3_key}")
            return True
        except ClientError as e:
            logger.error(f"Model download failed: {e}")
            return False
    
    def list_models(self, prefix: str = None):
        """List models in S3 bucket"""
        if not self.s3_client:
            return []
        
        try:
            prefix = prefix or AWS_CONFIG["s3_model_path"]
            response = self.s3_client.list_objects_v2(
                Bucket=AWS_CONFIG["s3_bucket"],
                Prefix=prefix
            )
            return [obj["Key"] for obj in response.get("Contents", [])]
        except ClientError as e:
            logger.error(f"Model listing failed: {e}")
            return []

