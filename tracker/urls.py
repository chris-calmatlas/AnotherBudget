"""
URL configuration for AnotherBudget project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.urls import path

from .views import *

urlpatterns = [
    path('', app.transactions, name='index'),

    path("auth/login/", auth.login_view, name="login"),
    path("auth/logout/", auth.logout_view, name="logout"),
    path("auth/register/", auth.register, name="register"),

    path("transactions/", transactions.list, name="listAllTransactions"),
    path("accounts/", accounts.list, name="listAllAccounts"),
    path("accounts/<str:accountId>/", accounts.getAccount, name="getAccount"),

    path("api/transactions/", transactions.api, {"transactionId":None}),
    path("api/transactions/<str:transactionId>/", transactions.api),
    path("api/accounts/", accounts.api, {"accountId":None}),
    path("api/accounts/<str:accountId>/", accounts.api),
]
