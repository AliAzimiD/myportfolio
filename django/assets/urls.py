"""URL configuration for the assets application.

This module defines all URL patterns for the assets app, including:
- Dashboard view
- Asset CRUD operations
- API endpoints using DRF router
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.dashboard import DashboardView
from .views.asset import AssetCreateView, AssetUpdateView, AssetDeleteView
from .views.api import CustomAssetViewSet

# Initialize DRF router for API endpoints
router = DefaultRouter()
router.register(r'assets', CustomAssetViewSet, basename='asset-api')

urlpatterns = [
    # Main dashboard view
    path('', DashboardView.as_view(), name='dashboard'),
    
    # Asset management URLs
    path('asset/add/', AssetCreateView.as_view(), name='asset-add'),
    path('asset/<int:pk>/edit/', AssetUpdateView.as_view(), name='asset-edit'),
    path('asset/<int:pk>/delete/', AssetDeleteView.as_view(), name='asset-delete'),
    
    # REST API endpoints
    path('api/', include(router.urls)),
]
