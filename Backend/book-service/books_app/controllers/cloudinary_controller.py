from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services import CloudinaryService
from ..utils import ResponseUtils
from ..serializers import CloudinaryUploadSerializer

class CloudinaryUploadView(APIView):

    def __init__(self, create_service: CloudinaryService = None):
        self.create_service = create_service or CloudinaryService()

    def post(self, request):
        try:
            print("Received image upload request")
            serializer = CloudinaryUploadSerializer(data=request.data)
            print("Serializer initialized with data:", request.data)

            if not serializer.is_valid():
                return ResponseUtils.error(
                    message="Invalid image upload request",
                    error=serializer.errors,
                    http_status=status.HTTP_400_BAD_REQUEST
                )

            print("Storing validated data")
            image_file = serializer.validated_data['image']
            print("Validated data stored, proceeding to upload", image_file)

            # Upload image to Cloudinary
            print("Calling CloudinaryService upload_image method")
            upload_result = self.create_service.upload_image(image_file)

            return ResponseUtils.success(
                message="Image uploaded successfully",
                data=upload_result,
                http_status=status.HTTP_200_OK
            )

        except Exception as e:
            return ResponseUtils.error(
                message="Image upload failed",
                error=str(e),
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
