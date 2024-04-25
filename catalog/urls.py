from django.urls import path
from django.views.decorators.cache import cache_page, never_cache

from catalog.apps import CatalogConfig
from catalog.views import PokemonListView, PokemonDetailView, BlogListView, BlogCreateView, BlogUpdateView, \
    BlogDeleteView, BlogDetailView, PokemonCreateView, IndexView, PokemonUpdateView, PokemonDeleteView, \
    CategoryCreateView, CategoryDetailView, CategoryUpdateView, CategoryDeleteView, categories

app_name = CatalogConfig.name

urlpatterns = [
    path('categories/', categories, name='categories'),
    path('create/', CategoryCreateView.as_view(), name='create_category'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='view_category'),
    path('update/<int:pk>/', CategoryUpdateView.as_view(), name='update_category'),
    path('<int:pk>/delete/', CategoryDeleteView.as_view(), name='delete_category'),
    path('', IndexView.as_view(), name='home_page'),
    # path('product/<int:pk>/', product, name='product'),
    path('catalog/', PokemonListView.as_view(), name='catalog'),
    path('create/', never_cache(PokemonCreateView.as_view()), name='create_product'),
    path('product/<int:pk>/', cache_page(60)(PokemonDetailView.as_view()), name='view_product'),
    path('product/<int:pk>/update/', never_cache(PokemonUpdateView.as_view()), name='update_product'),
    path('product/<int:pk>/delete/', PokemonDeleteView.as_view(), name='delete_product'),
    # path('catalog/', catalog, name='catalog'),
    path('blog/', BlogListView.as_view(), name='blog'),
    path('create/', never_cache(BlogCreateView.as_view()), name='create_blog'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='view_blog'),
    path('edit/<int:pk>/', never_cache(BlogUpdateView.as_view()), name='update_blog'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete_blog'),

]
