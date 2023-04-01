from rest_framework.views import APIView
from rest_framework.response import Response


class ChartsApi(APIView):
    def get(self, request, *args, **kwargs):
        data = [{'id': 1, "name": "Valera"}, {'id': 2, "name": "Anton"}]
        return Response(data)
