from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    ]

urlpatterns += [
    path('mybooks/', views.LoandBooksByUserListView.as_view(), name='my-borrowed'),
]

urlpatterns += [
    path('allloandbooks/', views.AllLoandBooksListView.as_view(), name='all-loand-books'),
]

urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]

urlpatterns += [
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
]

from django.contrib.auth import views as auth_views


urlpatterns += [
    path('accounts/login/', auth_views.LoginView.as_view(), name='account_login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='account_logout'),
]

urlpatterns += [
    path('bookinstance/create/', views.BookInstanceCreate.as_view(), name='bookinstance-create'),
    path('bookinstance/(?P<pk>[0-9]+)\\Z/update/', views.BookInstanceUpdate.as_view(), name='bookinstance-update'),
    path('bookinstance/(?P<pk>[0-9]+)\\Z/delete/', views.BookInstanceDelete.as_view(), name='bookinstance-delete'),
    path('bookinstance/(?P<pk>[0-9]+)\\Z', views.BookInstanceDetailView.as_view(), name='bookinstance-detail'),
    #path('bookinstance/<int:pk>', views.bookinstance_detail_view, name='bookinstance-detail'),
]