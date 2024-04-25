from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from catalog.forms import PokemonForm, VersionForm, ModeratorPokemonForm, CategoryForm
from catalog.models import Product, Blog, Version, Category
from catalog.services import get_categories_cache


@login_required
def categories(request):
    context = {
        'object_list': get_categories_cache(),
        'title': 'Категории покемонов',

    }
    return render(request, 'catalog/categories.html', context)


class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    permission_required = 'catalog.add_category'
    success_url = reverse_lazy('catalog:categories')


class CategoryDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Category
    permission_required = 'catalog.view_category'


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('catalog:categories')


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('catalog:categories')


class IndexView(TemplateView):
    template_name = 'catalog/home_page.html'


class PokemonListView(LoginRequiredMixin, ListView):
    model = Product


class PokemonCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = PokemonForm
    permission_required = 'catalog.add_product'
    success_url = reverse_lazy('catalog:catalog')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PokemonDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Product
    permission_required = 'catalog.view_product'


class PokemonUpdateView(LoginRequiredMixin, UpdateView):
    model = Product

    def get_success_url(self):
        return reverse('catalog:update_product', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST, instance=self.object)
        else:
            formset = VersionFormset(instance=self.object)

        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

    def get_form_class(self):

        if self.request.user == self.object.owner or self.request.user.is_staff:
            return PokemonForm
        elif self.request.user.groups.filter(name='moderators'):
            return ModeratorPokemonForm
        else:
            raise Http404


class PokemonDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = 'catalog.delete_product'
    success_url = reverse_lazy('catalog:catalog')


class BlogListView(LoginRequiredMixin, ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Blog
    permission_required = 'catalog.add_blog'
    fields = ('blog_title', 'preview', 'body', 'date_of_creation')
    success_url = reverse_lazy('catalog:blog')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.blog_title)
            new_blog.save()
        return super().form_valid(form)


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Blog
    fields = ('blog_title', 'preview', 'body')
    permission_required = 'catalog.change_blog'

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.blog_title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:view_blog', args=[self.kwargs.get('pk')])


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Blog
    permission_required = 'catalog.delete_blog'
    success_url = reverse_lazy('catalog:blog')
