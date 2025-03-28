from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.db import OperationalError


from . models import Order, OrderItem
from . import forms


class EditOrderView(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = forms.EditOrderForm
    template_name = 'orders/edit_order.html'

    def get_success_url(self):
        # order_id =self.kwargs['pk']
        # return reverse_lazy('order:edit_order', kwargs={'pk': order_id})
        return reverse_lazy('account:admin_dashboard')
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Order Updated successfully')
        return HttpResponseRedirect(self.get_success_url())
    

@login_required(login_url='account:login')
def delete_order(request, pk):
    order = Order.objects.get(pk=pk)
    order.delete()
    messages.success(request, 'Order was deleted successfully')
    return redirect('account:admin_dashboard')


def view_receipt(request, pk):
    try:
        order = Order.objects.get(pk=pk)
        order_items = OrderItem.objects.filter(order=order)
    except OperationalError:
        order = Order.objects.get(pk=pk)
        order_items = OrderItem.objects.filter(order=order)
    context = {'order':order, 'order_items':order_items}
    return render(request, 'orders/view_receipt.html', context)
        