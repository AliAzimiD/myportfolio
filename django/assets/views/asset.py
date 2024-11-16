from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from ..models import Asset, CustomAssetType

class AssetCreateView(LoginRequiredMixin, CreateView):
    model = Asset
    fields = ['name', 'asset_type', 'quantity', 'initial_price', 'purchase_date', 'exchange_name']
    template_name = 'assets/asset_form.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['custom_types'] = CustomAssetType.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        if 'new_type' in self.request.POST and self.request.POST['new_type']:
            custom_type = CustomAssetType.objects.create(
                name=self.request.POST['new_type'],
                user=self.request.user
            )
            form.instance.custom_type = custom_type
            form.instance.asset_type = 'other'
        elif self.request.POST.get('asset_type', '').startswith('custom_'):
            custom_type_id = self.request.POST['asset_type'].split('_')[1]
            form.instance.custom_type = CustomAssetType.objects.get(id=custom_type_id)
            form.instance.asset_type = 'other'
        
        form.instance.user = self.request.user
        return super().form_valid(form)

class AssetUpdateView(LoginRequiredMixin, UpdateView):
    model = Asset
    fields = ['name', 'asset_type', 'quantity', 'initial_price', 'purchase_date', 'exchange_name']
    template_name = 'assets/asset_form.html'
    success_url = reverse_lazy('dashboard')

class AssetDeleteView(DeleteView):
    model = Asset
    template_name = 'assets/asset_confirm_delete.html'
    success_url = '/'
