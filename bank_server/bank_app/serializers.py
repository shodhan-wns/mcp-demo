from rest_framework import serializers
from .models import Person, BankAccount, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class PersonDetailSerializer(serializers.ModelSerializer):
    accounts = BankAccountSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = '__all__'
