from rest_framework.routers import DefaultRouter
from .views import PersonViewSet, BankAccountViewSet, TransactionViewSet

router = DefaultRouter()
router.register('persons', PersonViewSet)
router.register('accounts', BankAccountViewSet, basename='bankaccount')
router.register('transactions', TransactionViewSet, basename='transaction')

urlpatterns = router.urls
