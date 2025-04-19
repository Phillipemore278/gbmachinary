from django.contrib import messages
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import login 
from django.views.generic import ListView, TemplateView, FormView, DetailView
from django.conf import settings

from . import emails
from . import forms

from store.models import Product, Media
from account.forms import RegistrationForm, UserLoginForm 



class HomeView(ListView):
    redirect_authenticated_user = True
    model = Product
    context_object_name = 'products'
    template_name = 'frontend/index.html'
    paginate_by= 8

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return HttpResponseRedirect(reverse_lazy('account:admin_dashboard'))
            else:
                return HttpResponseRedirect(reverse_lazy('account:customer_dashboard'))
        return super().dispatch(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):
    #    context = super(HomeView, self).get_context_data(**kwargs)
    #    return context


class AboutView(TemplateView):
    redirect_authenticated_user = True
    template_name = 'frontend/about.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return HttpResponseRedirect(reverse_lazy('account:admin_dashboard'))
            else:
                return HttpResponseRedirect(reverse_lazy('account:customer_dashboard'))
        return super().dispatch(request, *args, **kwargs)


class AllProductView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'frontend/products.html'


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'frontend/product_detail.html'

    def get_context_data(self, **kwargs):
       context = super(ProductDetailView, self).get_context_data(**kwargs)
       context['product_images'] = Media.objects.filter(product=self.object)
       return context


class ContactView(FormView):
    form_class = forms.ContactForm 
    success_url = reverse_lazy('frontend:contact')
    template_name = 'frontend/contact.html'  

    def form_valid(self, form):
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            final_message = render_to_string('emails/email_contact.html', 
                            {
                                'name': name,
                                'email': email,
                                'message': message,
                                'subject': subject
                            })

            if email and message and name:
                try:
                    emails.email_message_send(
                        'Message from '+ name,
                        final_message,
                        'contact@globalmachinary.com',
                    )
                    messages.success(self.request, "Your message was sent successfully, we will get back to you shortly")
                except:
                    messages.error(self.request, 'Something went wrong, please make sure your email is correct and try again')  
            else:
                message.error(self.request, 'Make sure all fields are entered and valid.')  
        return super(ContactView, self).form_valid(form)


class RegisterUserView(FormView):
    form_class = RegistrationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('frontend:login')
    template_name = 'frontend/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        messages.success(self.request, "Your account was created successfully, please login below")
        return super(RegisterUserView, self).form_valid(form)
    

class LoginUserView(LoginView):
    redirect_authenticated_user = True
    template_name = 'frontend/login.html'
    form_class = UserLoginForm

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy('account:admin_dashboard')
        else:
            return reverse_lazy('account:customer_dashboard')
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid Email or password, please try again')
        return self.render_to_response(self.get_context_data(form=form))

