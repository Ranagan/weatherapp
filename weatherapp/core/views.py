import datetime

from rest_framework.views import APIView
from rest_framework.response import Response

from weatherapp.core import services


class OutsideTempView(APIView):
  """ Defines endpoint handling the CSV processing
  """

  def get(self, request):
    context = services.get_outside_temp_context()

    return Response(context)
