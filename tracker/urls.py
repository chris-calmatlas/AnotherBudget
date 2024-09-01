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

    path("accounts/login/", auth.login_view, name="login"),
    path("accounts/logout/", auth.logout_view, name="logout"),
    path("accounts/register/", auth.register, name="register"),

    path("view/transactions/", transactions.listAll, name="listAllTransactions"),
    path("view/accounts/", accounts.listAll, name="listAllAccounts"),
    path("view/accounts/<str:accountId>/", accounts.getAccount, name="getAccount"),

    path("transactions/", transactions.api, {"transactionId":None}),
    path("transactions/<str:transactionId>/", transactions.api),
    path("accounts/", accounts.api, {"accountId":None}),
    path("accounts/<str:accountId>/", accounts.api),
]
