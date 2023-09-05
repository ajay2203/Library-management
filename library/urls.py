"""
URL configuration for library_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),  # Define a URL pattern for the root URL
    path('books/', views.book_list, name='book_list'),
    path('members/', views.member_list, name='member_list'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('issue_book/<int:book_id>/<int:member_id>/', views.issue_book, name='issue_book'),
    path('return_book/<int:transaction_id>/', views.return_book, name='return_book'),
    path('search/', views.book_search, name='book_search'),
    path('import_books/', views.import_books, name='import_books'),
    # Add more URL patterns for other views
]
