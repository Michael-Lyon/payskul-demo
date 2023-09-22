from django.urls import path

from . import views_v1

app_name="core"

urlpatterns = [
    path("logs/", views_v1.read_file, name="read_file"),
    path("get-banks/", views_v1.get_banks, name="bank_list"),
    path("get-limit/", views_v1.update_client_income_status, name="update_client_income_status"),
    path("details/", views_v1.DetailListView.as_view(), name="detail"),
    path("loan-list/", views_v1.loan_list, name="loan_list"),
    path("payment-slip/", views_v1.payment_slip, name="payment_slip"),
    path("validate-user-loan/", views_v1.validate_user_loan, name="validate_user_loan"),
    path("apply_loan/", views_v1.apply_loan, name="apply_loan"),
    path("webhook/", views_v1.webhook_view, name="webhook"),
    path("transactions/", views_v1.TransactionListCreateView.as_view(), name="transaction_list_create"),
    path("wallet/", views_v1.WalletListCreateView.as_view(), name="wallet_list_create"),
    path("confirm-payload/", views_v1.confirm_okra_link, name="confirm_okra_link"),
    path("card/", views_v1.CardListCreateView.as_view(), name="card_list_create"),
    path("service/", views_v1.ServiceListCreateView.as_view(), name="service"),
    path("service-category/", views_v1.ServiceCategoryListCreateView.as_view(), name="service_category"),
    path('connect-okra/', views_v1.link_account_okra_test, name='okra_link_demo'),
    path("extend-loan", views_v1.ExtendLoanView.as_view(), name="extend_loan"),
    path('loan-repayment', views_v1.LoanRepaymentView.as_view(), name='loan_repayment'),
    path('referrals', views_v1.ReferralView.as_view(), name='referrals'),
]
