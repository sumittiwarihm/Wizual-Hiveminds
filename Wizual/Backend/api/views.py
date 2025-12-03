# File: Backend/api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import ImageGenerationSerializer, VideoGenerationSerializer
from .services.imagen_service import generate_image_with_imagen3
from .services.videogen_service import generate_video_with_veo
from .models import GeneratedImage, IMAGE_STYLES ,GeneratedVideo


class GenerateImageView(APIView):
    
    permission_classes = [IsAuthenticated] 
    
    def post(self, request):
        try:
            user = request.user 
            
            serializer = ImageGenerationSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            prompt = serializer.validated_data["prompt"]
            style = serializer.validated_data["style"]

            image_urls = generate_image_with_imagen3(prompt, style)

            records = []
            for image_url in image_urls:
                record = GeneratedImage.objects.create(
                    user=user,  
                    prompt=prompt,
                    style=style,
                    image_url=image_url,
                )
                records.append({
                    "id": record.id,
                    "image_url": record.image_url,
                    "prompt": record.prompt,
                    "style": record.style,
                    "created_at": record.created_at.isoformat() if hasattr(record, 'created_at') else None, 
                })

            return Response(
                {
                    "success": True,
                    "count": len(records),
                    "images": records
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            print(f"[API Error] {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MyGeneratedImagesView(APIView):
    
    permission_classes = [IsAuthenticated] 
    
    def get(self, request):
        try:
            user = request.user 
            
            images = GeneratedImage.objects.filter(
                user=user  
            ).order_by("-created_at")

            data = [
                {
                    "id": img.id,
                    "prompt": img.prompt,
                    "style": img.style,
                    "image_url": img.image_url,
                    "created_at": img.created_at.isoformat() if hasattr(img, 'created_at') else None, 
                }
                for img in images
            ]
            
            return Response(
                {
                    "count": len(data),
                    "user": user.username,
                    "images": data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            print(f"[API Error] {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ImageStyleListView(APIView):
    
    permission_classes = [IsAuthenticated] 
    
    def get(self, request):
        try:
            return Response(
                [
                    {"key": key, "label": label}
                    for key, label in IMAGE_STYLES
                ],
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            print(f"[API Error] {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GenerateVideoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            user = request.user 
            serializer = VideoGenerationSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            prompt = serializer.validated_data["prompt"]
            style = serializer.validated_data["style"] 

            video_url = generate_video_with_veo(prompt, style) 

            if not video_url:
                 return Response(
                    {"error": "Video generation failed or returned no URL."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            record = GeneratedVideo.objects.create(
                user=user, 
                prompt=prompt,
                style=style, 
                video_url=video_url, 
            )
            response_data = {
                "id": record.id,
                "video_url": record.video_url,
                "prompt": record.prompt,
                "style": record.style,
                "created_at": record.created_at.isoformat(),
            }

            return Response(
                {
                    "success": True,
                    "message": "Video generation started and record saved.",
                    "video_record": response_data
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            print(f"[API Error] Failed to process video generation request: {str(e)}")
            return Response(
                {"error": "An internal server error occurred.", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )