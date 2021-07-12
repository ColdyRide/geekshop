from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from django.shortcuts import HttpResponseRedirect
from mainapp.models import Product, ProductCategories
from django.contrib.auth.decorators import user_passes_test
from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'users_list'
    ordering = ['-is_active', '-is_superuser', '-is_staff', 'username']
    extra_context = {'title': 'админка/пользователи'}


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    form_class = ShopUserRegisterForm
    success_url = reverse_lazy('admin_staff:users')
    extra_context = {'title': 'пользователи/создание'}


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    form_class = ShopUserAdminEditForm
    extra_context = {'title': 'пользователи/редактирование'}

    def get_success_url(self):
        return reverse_lazy('admin_staff:user_update', args=[self.object.pk])


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserDeleteView(DeleteView):
    model = ShopUser
    success_url = reverse_lazy('admin_staff:users')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class CategoriesListView(ListView):
    model = ProductCategories
    template_name = 'adminapp/categories.html'
    extra_context = {'title': 'админка/категории'}
    context_object_name = 'categories'


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class CategoryCreateView(CreateView):
    model = ProductCategories
    template_name = 'adminapp/category_update.html'
    form_class = ProductCategoryEditForm
    extra_context = {'title': 'категории/создание'}
    success_url = reverse_lazy('admin_staff:categories')


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class CategoryUpdateView(UpdateView):
    model = ProductCategories
    template_name = 'adminapp/category_update.html'
    form_class = ProductCategoryEditForm
    extra_context = {'title': 'категории/редактирование'}

    def get_success_url(self):
        return reverse_lazy('admin_staff:category_update', args=[self.object.pk])


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class CategoryDeleteView(DeleteView):
    model = ProductCategories
    success_url = reverse_lazy('admin_staff:categories')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductsListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'
    paginate_by = 4
    context_object_name = 'products'
    extra_context = {'title': 'админка/продукты'}

    def get_queryset(self):
        pk = self.kwargs['pk']
        if pk == 1:
            return Product.objects.all().order_by('name')
        return Product.objects.filter(category__pk=pk).order_by('name')


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    extra_context = {'title': 'продукты/создание'}
    form_class = ProductEditForm
    template_name = 'adminapp/product_update.html'

    def get_initial(self):
        return {'category': self.kwargs['pk']}

    def get_success_url(self):
        return reverse_lazy('admin_staff:products', args=[self.object.category.id])


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductDetailedView(DetailView):
    model = Product
    extra_context = {'title': 'продукты/детали'}
    template_name = 'adminapp/product_read.html'


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    extra_context = {'title': 'продукты/редактирование'}
    template_name = 'adminapp/product_update.html'
    form_class = ProductEditForm

    def get_success_url(self):
        return reverse_lazy('admin_staff:product_update', args=[self.object.pk])


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product

    def get_success_url(self):
        return reverse_lazy('admin_staff:products', args=[self.object.category.id])

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

