import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary import CloudinaryImage
import json

class CloudinaryRepository:
    
    @staticmethod
    def upload_file(file, public_id=None, folder=None):
        """Upload file to Cloudinary"""
        try:
            upload_result = cloudinary.uploader.upload(
                file,
                public_id=public_id,
                folder=folder,
                unique_filename=True,
                overwrite=True
            )
            return upload_result
        except Exception as e:
            raise Exception(f"Cloudinary upload failed: {str(e)}")
    
    @staticmethod
    def get_asset_info(public_id):
        """Get asset information from Cloudinary"""
        try:
            asset_info = cloudinary.api.resource(public_id)
            return asset_info
        except Exception as e:
            raise Exception(f"Failed to get asset info: {str(e)}")
    
    @staticmethod
    def generate_url(public_id, transformations=None):
        """Generate URL for the asset with optional transformations"""
        try:
            if transformations:
                url = CloudinaryImage(public_id).build_url(**transformations)
            else:
                url = CloudinaryImage(public_id).build_url()
            return url
        except Exception as e:
            raise Exception(f"URL generation failed: {str(e)}")
    
    @staticmethod
    def update_tags(public_id, tags):
        """Update tags for an asset"""
        try:
            update_resp = cloudinary.api.update(public_id, tags=tags)
            return update_resp
        except Exception as e:
            raise Exception(f"Tag update failed: {str(e)}")