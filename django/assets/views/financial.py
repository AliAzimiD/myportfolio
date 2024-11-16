# Remove or comment out the entire content of this file.
# from django.views.generic import ListView, CreateView, UpdateView, DeleteView
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.urls import reverse_lazy
# from ..models import FinancialRecord, Asset

# class FinancialRecordListView(LoginRequiredMixin, ListView):
#     model = FinancialRecord
#     template_name = 'assets/financial_records.html'
#     context_object_name = 'records'

#     def get_queryset(self):
#         return FinancialRecord.objects.filter(user=self.request.user)

# class FinancialRecordCreateView(LoginRequiredMixin, CreateView):
#     model = FinancialRecord
#     fields = ['date', 'record_type', 'amount', 'currency', 'description', 'asset']
#     template_name = 'assets/financial_record_form.html'
#     success_url = reverse_lazy('financial-records')

#     def get_form(self, form_class=None):
#         form = super().get_form(form_class)
#         form.fields['asset'].queryset = Asset.objects.filter(user=self.request.user)
#         return form

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)

# class FinancialRecordUpdateView(LoginRequiredMixin, UpdateView):
#     model = FinancialRecord
#     fields = ['date', 'record_type', 'amount', 'currency', 'description', 'asset']
#     template_name = 'assets/financial_record_form.html'
#     success_url = reverse_lazy('financial-records')

#     def get_form(self, form_class=None):
#         form = super().get_form(form_class)
#         form.fields['asset'].queryset = Asset.objects.filter(user=self.request.user)
#         return form

# class FinancialRecordDeleteView(LoginRequiredMixin, DeleteView):
#     model = FinancialRecord
#     success_url = reverse_lazy('financial-records')
#     template_name = 'assets/financial_record_confirm_delete.html'