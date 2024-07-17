import re

from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView, FormView, DetailView, DeleteView, UpdateView
from django.views.generic.list import BaseListView

from apps.forms import RegisterForm, OrderForm, ProfileForm
from apps.models import C, P, W, User, Booking


def kim(request):
    context = {
        "categories": C.objects.all(),
        "products": P.objects.all()
    }
    return TemplateResponse(request, 'apps/product-list.html', context=context)


def smth(request, slug):
    context = {
        "pr": P.objects.filter(c_id=slug),
        "categories": C.objects.all()
    }
    return TemplateResponse(request, 'apps/prod.html', context=context)


def smth2(request, slug):
    context = {
        "pro": P.objects.filter(slug=slug),
        "categories": C.objects.all()
    }
    return TemplateResponse(request, 'apps/product-details.html', context=context)


class ProductListView(ListView):
    # model = Product
    template_name = 'apps/product-list.html'
    context_object_name = 'products'


class HomeView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'apps/product-list.html'
    success_url = reverse_lazy('home')


class RegisterFormView(FormView):
    template_name = 'apps/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return redirect('login')


class CustomLoginView(TemplateView):
    template_name = 'apps/login.html'

    def post(self, request, *args, **kwargs):
        phone_number = re.sub('\D', '', request.POST.get('phone_number'))
        user = User.objects.filter(phone_number=phone_number).first()
        if user:
            user = authenticate(request, username=user.phone_number, password=request.POST['password'])

            if user:
                login(request, user)
                return redirect('home')
            else:
                context = {
                    "messages_error": ["Invalid password or phone_number"]
                }
                return render(request, template_name='apps/login.html', context=context)
        else:
            return redirect('login')


def order(request, slug):
    context = {
        "order": P.objects.filter(slug=slug).first(),
        "categories": C.objects.all()
    }
    return TemplateResponse(request, 'apps/orders/order.html', context=context)


class OrderDetailView(DetailView, FormView):
    form_class = OrderForm
    model = P
    template_name = 'apps/orders/order.html'
    context_object_name = 'order'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        if form.is_valid():
            form = form.save(commit=False)
            form.user = self.request.user
            form.save()
        return render(self.request, 'apps/orders/completed-order.html', {'form': form})


# class OrFormView(FormView):
#     success_url = reverse_lazy('complete-order')
#     def form_valid(self, form):
#         if form.is_valid():
#             form.save()
#         return redirect('complete-order')


def kimsan(request):
    return TemplateResponse(request, 'apps/orders/completed-order.html')


class WListView(View):
    # queryset = W.objects.all().filter()
    # context_object_name = 'wishlists'
    # template_name = 'apps/wishlist/completed-wishlist.html'

    # paginate_by = 2



    def get(self, request):
        c = C.objects.all()
        query = W.objects.filter(user_id=self.request.user)
        return render(request, 'apps/wishlist/completed-wishlist.html',{'wishlists':query,'categories':c})

    # def get_context_data(self, **kwargs):
    #     data = super().get_context_data()
    #     data['categories'] = C.objects.all()
    #     return data


class MyOrdersView(View):
    # queryset = Booking.objects.all()
    # context_object_name = 'orders'
    # template_name = 'apps/orders/order-list.html'
    #
    # # paginate_by = 2
    #
    # def get_context_data(self, **kwargs):
    #     data = super().get_context_data()
    #     data['categories'] = C.objects.all()
    #     return data

    def get(self, request):
        c = C.objects.all()
        query = Booking.objects.filter(user_id=self.request.user)
        return render(request, 'apps/orders/order-list.html',{'orders':query,'categories':c})



class LikeView(View):
    def get(self, request, slug, *args, **kwargs):
        wishlist, created = W.objects.get_or_create(product_id=slug, user=self.request.user)
        if not created:
            wishlist.delete()
        return redirect('home')


class CategoryListView(ListView):
    queryset = P.objects.all()
    template_name = 'apps/product-list.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data['categories'] = C.objects.all()
        return data


class LikeDeleteView(View):
    def get(self,request,pk,*args,**kwargs):
        W.objects.filter(id=pk).delete()
        return redirect('wishlist')

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data['categories'] = C.objects.all()
        return data


class MyOrderDelete(View):

    def get(self,request,pk,*args,**kwargs):
        Booking.objects.filter(id=pk).delete()
        return redirect('my-orders')

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data['categories'] = C.objects.all()
        return data


class ProfileFormView(FormView):
    template_name = 'apps/Profile/profile.html'
    form_class = ProfileForm

    def form_valid(self, form):
        if form.is_valid():
            # form.cleaned_data['password'] = make_password(form.cleaned_data['password'])
            User.objects.filter(pk=self.request.user.pk).update(**form.cleaned_data)
        return redirect('profile')

