from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import (
   ListView, TemplateView, CreateView,
   DeleteView, DetailView, FormView, UpdateView
   )
from django.http import HttpResponse
from django.contrib.auth import logout
from django.core.paginator import Paginator

from .forms import CustomerChangePasswordForm
from .models import Customer
from order.models import Order, OrderItem
from store.models import Product
from store.forms import AddProductForm, MediaFormSet, EditMediaFormSet


class AdminDashboard(LoginRequiredMixin, ListView):
    model = Customer
    context_object_name = 'customers'
    template_name = 'account/admin_dashboard.html'
    paginate_by = 8  # This is for customer pagination

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponse("Error handler content", status=400)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(is_staff=False)

    def get_context_data(self, **kwargs):
        context = super(AdminDashboard, self).get_context_data(**kwargs)
        context['orders'] = Order.objects.all()

        # Get all products and paginate them
        product_list = Product.objects.all()
        paginator = Paginator(product_list, 6)  # Show 8 products per page
        page = self.request.GET.get('product_page')  # Use a different name to avoid conflict with customer pagination
        products = paginator.get_page(page)

        context['products'] = products  # Paginated products
        return context


class DeleteCustomerView(LoginRequiredMixin, DeleteView):
   model = Customer
   template_name = 'account/delete_customer.html'
   context_object_name = 'customer'
   success_url = reverse_lazy('account:admin_dashboard')

   def form_valid(self, form):
      messages.success(self.request, "The customer was deleted successfully.")
      return super(DeleteCustomerView,self).form_valid(form)


class AddProductView(LoginRequiredMixin, CreateView):
   form_class = AddProductForm
   model = Product
   template_name = "store/product_create_or_update.html"
   success_url = reverse_lazy('account:admin_dashboard')

   def form_valid(self, form):
      ctx = self.get_context_data()
      media_form = ctx['media_form']
      
      if media_form.is_valid() and form.is_valid():      
         prod = form.save()
         media_form.instance = prod
         media_form.save()
         messages.success(self.request, 'Product was added successfully')
      return super(AddProductView, self).form_valid(form)

   def get_context_data(self, **kwargs):
      ctx = super(AddProductView,self).get_context_data(**kwargs)
      ctx['title'] = 'Add New Product'
      if self.request.POST:
         ctx['form']= AddProductForm(self.request.POST)
         ctx['media_form']= MediaFormSet(self.request.POST, self.request.FILES)
      else:
         ctx['form']= AddProductForm()
         ctx['media_form']= MediaFormSet()
      return ctx
   

class EditProductView(LoginRequiredMixin, UpdateView):
   form_class = AddProductForm
   model = Product
   template_name = "store/update.html"
   success_url = reverse_lazy('account:admin_dashboard')

   def form_valid(self, form):
      """
      Handles the submission of both the product form and the media formset.
      """
      # Save the product form but don't commit to the database yet
      self.object = form.save(commit=False)

      # Get the media formset from the context
      ctx = self.get_context_data()
      media_form = ctx['media_form']

      if media_form.is_valid():
         # Save the product first (now that it's ready)
         self.object.save()

         # Ensure the formset has the correct instance of the Product
         media_form.instance = self.object

         # Save the media formset (existing and new media)
         media_form.save()

         messages.success(self.request, 'Product was updated successfully')
      else:
         # If the formset is invalid, return the form with errors
         return self.form_invalid(form)

      return super(EditProductView, self).form_valid(form)

   def form_invalid(self, form):
      """
      This method handles the invalid form submission for both product and formset.
      """
      ctx = self.get_context_data(form=form)
      messages.error(self.request, 'There was an error updating the product. Please check the form for details.')
      return self.render_to_response(ctx)

   def get_context_data(self, **kwargs):
      """
      Overriding the context to include both the product form and the media formset.
      """
      ctx = super(EditProductView, self).get_context_data(**kwargs)
      ctx['title'] = 'Edit Product'

      if self.request.POST:
         # Pass the product instance to both the form and the formset
         ctx['form'] = AddProductForm(self.request.POST, instance=self.object)
         ctx['media_form'] = EditMediaFormSet(self.request.POST, self.request.FILES, instance=self.object)
      else:
         # Pass the existing product instance for GET requests
         ctx['form'] = AddProductForm(instance=self.object)
         ctx['media_form'] = EditMediaFormSet(instance=self.object)

      return ctx






@login_required(login_url='account:login')
def delete_product(request, pk):
   product = Product.objects.get(pk=pk)
   product.delete()
   messages.success(request, 'product was deleted successfully')
   return redirect('account:admin_dashboard')


class CustomerDashboard(LoginRequiredMixin, TemplateView):
   template_name = 'account/customer_dashboard.html'

   def get_context_data(self, **kwargs):
      context = super(CustomerDashboard, self).get_context_data(**kwargs)
      context['orders'] = Order.objects.filter(user=self.request.user)
      return context


class CustomerChangePasswordView(LoginRequiredMixin, FormView):
   model = Customer
   template_name = 'account/customer_change_password.html'
   form_class = CustomerChangePasswordForm
   success_url = reverse_lazy('frontend:login')

   def get_form_kwargs(self):
      kwargs = super().get_form_kwargs()
      kwargs['user'] = self.request.user
      return kwargs

   def form_valid(self, form):
      if form.is_valid():
         form.save()
         messages.success(self.request, 'Your Password was changed successfully, login with your new password')
      return super(CustomerChangePasswordView, self).form_valid(form)



class CustomerOrderDetails(LoginRequiredMixin, DetailView):
   model = Order
   context_object_name = 'order'
   template_name = 'account/customer_order_detail.html'

   def get_queryset(self, **kwargs):
      qs = super().get_queryset(**kwargs)
      return qs.filter(user=self.request.user)

   def get_context_data(self, **kwargs):
      context = super( CustomerOrderDetails, self).get_context_data(**kwargs)
      context['order_items'] = OrderItem.objects.filter(order=self.object)
      return context
   

def logout_user(request):
   logout(request)
   return redirect('frontend:login')

