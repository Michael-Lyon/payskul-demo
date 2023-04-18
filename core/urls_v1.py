from django.urls import path

from . import views_v1

app_name="core"

urlpatterns = [
    path("logs/", views_v1.read_file, name="read_file"),
    path("get-banks/", views_v1.get_banks, name="bank_list"),
    path("details/", views_v1.DetailListView.as_view(), name="detail"),
    path("loan-list/", views_v1.loan_list, name="loan_list"),
    path("validate-user-loan/", views_v1.validate_user_loan, name="validate_user_loan"),
    path("apply_loan/", views_v1.apply_loan, name="apply_loan"),
    path("top_wallet/", views_v1.top_wallet, name="top_wallet"),
    path("transactions/", views_v1.TransactionListCreateView.as_view(), name="transaction_list_create"),
    path("wallet/", views_v1.WalletListCreateView.as_view(), name="wallet_list_create"),
    path("card/", views_v1.CardListCreateView.as_view(), name="card_list_create"),
    path("service/", views_v1.ServiceListCreateView.as_view(), name="service"),
    path("service-category/", views_v1.ServiceCategoryListCreateView.as_view(), name="service_category"),
    
]
