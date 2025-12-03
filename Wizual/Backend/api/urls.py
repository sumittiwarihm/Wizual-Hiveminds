from django.urls import path
from .views import (
    GenerateImageView,
    MyGeneratedImagesView,
    ImageStyleListView,
    GenerateVideoView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
     TokenVerifyView
)

urlpatterns = [
    path("token/",TokenObtainPairView.as_view(),name="getToken"),
    path("token/refresh/",TokenRefreshView.as_view(),name="refreshToken"),
    path("token/verify/",TokenVerifyView.as_view(),name="verifyToken"),
    path("generate-image/", GenerateImageView.as_view(), name="generate-image"),
    path("my-images/", MyGeneratedImagesView.as_view(), name="my-images"),
    path("image-styles/", ImageStyleListView.as_view(), name="image-styles"),
    path("generate-video/",GenerateVideoView.as_view(),name="generate-image")  
]

