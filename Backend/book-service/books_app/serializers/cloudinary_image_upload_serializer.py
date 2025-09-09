from rest_framework import serializers
import os
import imghdr

class CloudinaryUploadSerializer(serializers.Serializer):
    
    image = serializers.ImageField(required=True)

    def validate_image(self, data):
        print("The data size is ", data.size)
        # ✅ Check file size (limit to 5MB)
        max_size = 5 * 1024 * 1024 
        if data.size > max_size:
            raise serializers.ValidationError("Image size should not exceed 5MB.")
        
        # ✅ Check image file type (sanity check)
        file_type = imghdr.what(data)
        if file_type not in ['jpeg', 'png', 'gif', 'bmp', 'tiff', 'jpg']:
            raise serializers.ValidationError("Unsupported image type.")
        
        # ✅ Sanitize file name
        data.name = os.path.basename(data.name).replace(" ", "_")
        return data
