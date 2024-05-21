from django.urls import path, re_path
from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordChangeDoneView, 
    PasswordChangeView
)

from app.views import (
    main, product, api
)

urlpatterns = [
    # login
    path('accounts/login/', LoginView.as_view()),
    path('changepassword/', PasswordChangeView.as_view(
        template_name = 'registration/change_password.html'), name='editpassword'),
    path('changepassword/done/', PasswordChangeDoneView.as_view(
        template_name = 'registration/afterchanging.html'), name='password_change_done'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # product
    path('api/product/list', product.ProductListAPIView.as_view(), name="api_product_list"),
    path('api/product/<int:id>', product.ProductDetailAPIView.as_view(), name="api_product_detail"),

    path("api/get-personal-data", api.PersonalDataByPassport.as_view()),

    # branch
    path('api/branch/list', api.BranchListAPIView.as_view(), name='api_branch_list'),

    # files
    re_path(r'^files/(?P<path>.*)$', main.get_file),


]
