from rest_framework import serializers

from .models import Customer, Item, Deal


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['customer', ]

    def create(self, validated_data):
        try:
            customer = Customer.objects.get(customer=validated_data.get('customer'))
        except Customer.DoesNotExist:
            customer = Customer.objects.create(**validated_data)
            customer.save()
        return customer


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['item', ]

    def create(self, validated_data):
        try:
            item = Item.objects.get(item=validated_data.get('item'))
        except Item.DoesNotExist:
            item = Item.objects.create(**validated_data)
            item.save()
        return item


class DealSerializer(serializers.ModelSerializer):

    customer = serializers.CharField()
    item = serializers.CharField()

    class Meta:
        model = Deal
        fields = '__all__'

    def create(self, validated_data):
        customer_data = validated_data.get('customer')
        item_data = validated_data.get('item')

        customer = CustomerSerializer().create({'customer': customer_data})
        item = ItemSerializer().create({'item': item_data})

        deal = Deal.objects.create(customer=customer,
                                   item=item,
                                   total=validated_data.get('total'),
                                   quantity=validated_data.get('quantity'),
                                   date=validated_data.get('date'))
        return deal
