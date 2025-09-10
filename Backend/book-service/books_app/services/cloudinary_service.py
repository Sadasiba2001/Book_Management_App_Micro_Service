from ..repositories import CloudinaryRepository

class CloudinaryService:

    def __init__(self, create_repo: CloudinaryRepository = None):
        self.create_repo = create_repo or CloudinaryRepository()

    def upload_image(self, file, folder="books"):
        """Upload image and return optimized URL"""
        try:
            
            # Upload file to Cloudinary
            upload_result = self.create_repo.upload_file(file, folder=folder)

            # Get public_id from upload result
            public_id = upload_result['public_id']
            
            # Auto-tag based on image size
            asset_info = self.create_repo.get_asset_info(public_id)
            tags = CloudinaryService._generate_size_tags(asset_info["width"])
            self.create_repo.update_tags(public_id, tags)

            # Generate optimized URL with transformations
            transformations = {
                'width': 800,
                'height': 600,
                'crop': 'fill',
                'quality': 'auto',
                'format': 'auto'
            }

            optimized_url = self.create_repo.generate_url(public_id, transformations)

            return {
                'url': optimized_url,
                'public_id': public_id,
                'format': upload_result['format'],
                'width': upload_result['width'],
                'height': upload_result['height'],
                'tags': tags
            }
            
        except Exception as e:
            raise Exception(f"Image upload service failed: {str(e)}")
    
    @staticmethod
    def _generate_size_tags(width):
        """Generate tags based on image width"""
        if width > 900:
            return ["large"]
        elif width > 500:
            return ["medium"]
        else:
            return ["small"]