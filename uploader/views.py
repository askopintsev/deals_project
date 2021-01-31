from rest_framework.views import APIView
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework_csv.parsers import CSVParser
from django.db.models import Sum
from django.http import JsonResponse

from .serializers import DealSerializer
from .models import Customer, Deal


def search_for_gems(gems_dict, customer_id):
    """Function performs filtering of gems names
    with requirements of -  gem must be purchased minimum by 2 users"""

    result_gems_set = set()
    current_list = gems_dict[customer_id]
    for i in gems_dict.values():
        if current_list == i:
            continue
        x = current_list.intersection(i)
        result_gems_set.update(x)
    return list(result_gems_set)


class UploadFileView(APIView):
    """Endpoint for csv import"""

    parser_classes = (CSVParser,) + tuple(api_settings.DEFAULT_PARSER_CLASSES)

    def post(self, request):

        serializer = DealSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return JsonResponse(data={'Status: Error, Desc: Некорректные данные в файле'},
                                status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(data={'Status': 'OK'}, safe=False, status=status.HTTP_200_OK)


class ResultsView(APIView):
    """Endpoint to get top-5 users"""

    def get(self, request):

        # receiving top-5 users by spent money
        queryset = Customer.objects.select_related('deal') \
                                   .values('id', 'customer') \
                                   .annotate(spent_money=Sum('deal__total'))  \
                                   .order_by('-spent_money')[:5]

        # receiving gems list for each user from top-5
        gems_dict = {}
        for customer in queryset:
            gems_data = Deal.objects.select_related('item') \
                                   .values('item__item').distinct() \
                                   .filter(customer=customer['id'])
            gems_set = [item['item__item'] for item in gems_data]
            gems_dict[customer['id']] = set(gems_set)

        # creating response with format from requirements
        result = []
        for customer in queryset:
            response = {}
            response['username'] = customer['customer']
            response['spent_money'] = customer['spent_money']
            response['gems'] = search_for_gems(gems_dict, customer['id'])
            result.append(response)

        return JsonResponse(data={'response': result}, safe=False, status=status.HTTP_200_OK)
