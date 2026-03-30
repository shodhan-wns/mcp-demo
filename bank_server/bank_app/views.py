from rest_framework import viewsets, filters
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .models import Person, BankAccount, Transaction
from .serializers import PersonSerializer, PersonDetailSerializer, BankAccountSerializer, TransactionSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PersonDetailSerializer
        return PersonSerializer


@extend_schema(
    parameters=[
        OpenApiParameter('person_id', OpenApiTypes.UUID, description='Filter by person ID'),
    ]
)
class BankAccountViewSet(viewsets.ModelViewSet):
    serializer_class = BankAccountSerializer

    def get_queryset(self):
        qs = BankAccount.objects.all()
        person_id = self.request.query_params.get('person_id')
        if person_id:
            qs = qs.filter(person_id=person_id)
        return qs


@extend_schema(
    parameters=[
        OpenApiParameter('account_id', OpenApiTypes.UUID, required=True, description='Filter by account ID'),
        OpenApiParameter('last_n', OpenApiTypes.INT, default=10, description='Return only the last N transactions'),
    ]
)
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        qs = Transaction.objects.order_by('-createdAt')
        account_id = self.request.query_params.get('account_id')
        if account_id:
            qs = qs.filter(bank_account_id=account_id)
        last_n = int(self.request.query_params.get('last_n', 10))
        qs = qs[:last_n]
        return qs
