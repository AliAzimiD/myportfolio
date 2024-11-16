# assets/views/websocket.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import asyncio
import logging

from assets.services.ramzinex_orderbook import import_ramzinex_orderbook

logger = logging.getLogger(__name__)

class RamzinexWebSocketView(APIView):
    """Handle WebSocket connections to Ramzinex exchange."""
    
    def post(self, request):
        """Start WebSocket connection for given trading pair."""
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