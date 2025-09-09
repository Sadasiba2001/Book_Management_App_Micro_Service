import cloudinary
import os
from dotenv import load_dotenv

load_dotenv()

def configure_cloudinary():
    """Configure Cloudinary with environment variables"""
    cloudinary.config(
        cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
        api_key=os.getenv('CLOUDINARY_API_KEY'),
        api_secret=os.getenv('CLOUDINARY_API_SECRET'),
        secure=True
    )
    
    # Verify configuration
    if not all([cloudinary.config().cloud_name, cloudinary.config().api_key]):
        raise Exception("Cloudinary configuration missing. Check environment variables.")