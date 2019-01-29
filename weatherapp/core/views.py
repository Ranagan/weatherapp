import datetime

from django.http import HttpResponse
from rest_framework.views import APIView

from weatherapp.core import services


class OutsideTempView(APIView):
  """ Defines endpoint to get the Outside Temperature data
  """

  def get(self, request):
    context = services.get_outside_temp_context()

    response = HttpResponse("this is a big ole test", content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="outside_temp.txt"'
    return response


class HiTempView(APIView):
  """ Defines endpoint to get the Hi Temp data.
  """

  def get(self, request):
    context = services.get_hi_temp_context()

    response = HttpResponse("this is a big ole test", content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="hi_temp.txt"'
    return response


class ForecastView(APIView):
  """ Defines endpoint to get the forecast data.
  """

  def get(self, request):
    context = services.get_forecast_context()

    response = HttpResponse("this is a big ole test", content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="forecast.txt"'
    return response
