from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
import asyncio
import logging
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from rest_framework.permissions import IsAuthenticated

from .models import Asset, Transaction
from .serializers import CustomAssetSerializer, TransactionSerializer
from .services.exchange_service import import_ramzinex_balances, import_ramzinex_transactions
from .services.ramzinex_orderbook import import_ramzinex_orderbook

logger = logging.getLogger(__name__)

class CustomAssetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing custom crypto assets.
    
    Provides CRUD operations for CustomAsset model with additional
    validation and response handling.
    """
    permission_classes = [IsAuthenticated]
    queryset = Asset.objects.all()
    serializer_class = CustomAssetSerializer

    def get_queryset(self):
        return Asset.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new custom asset with validation.
        
        Returns:
            Response: 201 CREATED with asset data if valid
                     400 BAD REQUEST if validation fails
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        asset = self.get_object()
        serializer = self.get_serializer(asset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing crypto transactions.
    
    Handles creation, reading, updating and deletion of Transaction records.
    """
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new transaction with validation.
        
        Returns:
            Response: 201 CREATED if valid, 400 BAD REQUEST if invalid
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImportRamzinexBalancesView(APIView):
    """
    API endpoint to import asset balances from Ramzinex exchange.
    
    POST: Fetches current balances and creates/updates CustomAsset records.
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        imported_assets = import_ramzinex_balances()
        if not imported_assets:
            return Response({"error": "Failed to import balances from Ramzinex"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = CustomAssetSerializer(imported_assets, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ImportRamzinexTransactionsView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        imported_transactions = import_ramzinex_transactions()
        if not imported_transactions:
            return Response({"error": "Failed to import transactions from Ramzinex"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = TransactionSerializer(imported_transactions, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class StartRamzinexWebSocketView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        pair_id = request.data.get('pair_id')
        if not pair_id:
            return Response(
                {"error": "pair_id is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            asyncio.run(import_ramzinex_orderbook(pair_id))
            return Response(
                {"message": "WebSocket connection started"}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Failed to start WebSocket connection: {str(e)}")
            return Response(
                {"error": "Failed to start WebSocket connection"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Main dashboard view displaying assets summary and recent transactions.
    
    Provides context with:
    - List of all assets
    - 5 most recent transactions
    """
    login_url = '/login/'
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assets'] = Asset.objects.all()
        context['recent_transactions'] = Transaction.objects.all().order_by('-transaction_date')[:5]
        return context

class AssetCreateView(LoginRequiredMixin, CreateView):
    model = Asset
    template_name = 'assets/asset_form.html'
    fields = ['name', 'asset_type', 'quantity', 'initial_price', 'purchase_date', 'exchange_name']
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class AssetUpdateView(LoginRequiredMixin, UpdateView):
    model = Asset
    template_name = 'assets/asset_form.html'
    fields = ['name', 'asset_type', 'quantity', 'initial_price', 'purchase_date', 'exchange_name']
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        return Asset.objects.filter(user=self.request.user)

class AssetDeleteView(LoginRequiredMixin, DeleteView):
    model = Asset
    success_url = reverse_lazy('dashboard')
    template_name = 'assets/asset_confirm_delete.html'

    def get_queryset(self):
        return Asset.objects.filter(user=self.request.user)
