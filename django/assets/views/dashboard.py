"""
Dashboard view module.

This module contains the main dashboard view that displays:
- Portfolio overview
- Asset summary
"""
from django.db.models import Sum, F
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Asset

class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Main dashboard view for displaying portfolio overview.
    
    Attributes:
        template_name: The template used to render the dashboard
        login_url: URL to redirect if user is not authenticated
    """
    template_name = 'assets/dashboard.html'
    login_url = '/login/'
    
    def get_context_data(self, **kwargs):
        """
        Enhance the template context with:
        - List of user's assets
        - Portfolio statistics
        """
        context = super().get_context_data(**kwargs)
        
        # Get user's assets
        user_assets = Asset.objects.filter(user=self.request.user)
        
        # Calculate total value using expression
        portfolio_stats = user_assets.aggregate(
            total_value_usd=Sum(F('quantity') * F('initial_price')),
            total_purchase_value=Sum(F('quantity') * F('initial_price'))
        )

        context.update({
            'assets': user_assets,
            'portfolio_stats': portfolio_stats
        })
        return context