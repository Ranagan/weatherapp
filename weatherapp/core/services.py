import collections
import datetime
import io

from weatherapp.core import constants

from django.core.cache import cache

import requests
import pandas


def get_outside_temp_context():
  """ Gets and returns the context for the Outside Temperatures View
  """
  highs = _get_highest_temps()
  times = []
  temps = []
  for value in highs.values():
    times.append(datetime.datetime.strptime(value['time'], '%H:%M'))

  for k, v in highs.items():
    temps.append({'date': k, 'temp': v['temp']})

  avg_time = _get_average_time(times)
  most_common = _get_most_common_time(times)
  top_temps = _get_top_temps(temps)

  return {
      'time': avg_time,
      'most_common_time': most_common,
      'top_temps': top_temps,
  }


def get_hi_temp_context():
  """ Gets and returns the context for the Hi Temp View
  """
  valid_entries = _get_hi_temp_range()
  return valid_entries


def get_forecast_context():
  """ Gets and returns the context for the Forecast View
  """
  forecast = _calculate_forecast()
  return forecast


def _get_weather_data():
  """ Fetches the weather data CSV from the given URL
  """
  try:
    response = requests.get(constants.WEATHER_CSV_URL)
  except requests.exceptions.RequestException as e:
    raise e

  data = response.content.decode('utf-8')

  df = pandas.read_csv(
      io.StringIO(data), usecols=constants.WEATHER_CSV_FIELDNAMES)

  cache.set('weather_df', df, 86400)

  return df


def _get_weather_df():
  """ Fetches the dataframe from the cache. If none are available,
  it fetches a new one.
  """
  if cache.get('weather_df') is None:
    return _get_weather_data()

  return cache.get('weather_df')


def _create_date(date_str):
  """ Creates a datetime from the str given in the csv.
  """
  return datetime.datetime.strptime(date_str, '%d/%m/%Y')


def _calculate_average(arr):
  total = sum(item for item in arr)
  avg = total / len(arr)
  return avg


def _get_highest_temps():
  """ Creates a dictionary of the highest temperatures
  """
  df = _get_weather_df()
  unique_dates = df.Date.unique()
  highest_values = {}

  for date in unique_dates:
    # Initialise the highest value to be overwritten
    highest_values.update({date: {'time': 0, 'temp': 0}})
    rows = df.loc[df['Date'] == date]

    for index, row in rows.iterrows():
      if row['Outside Temperature'] > highest_values[row['Date']]['temp']:
        highest_values.update({
            date: {
                'time': row['Time'],
                'temp': row['Outside Temperature']
            }
        })

  return highest_values


def _get_average_time(times):
  """ Calculates and returns the average time in a list of times
  """
  total = sum(dt.hour * 3600 + dt.minute * 60 + dt.second for dt in times)
  avg = total / len(times)
  return datetime.datetime.fromtimestamp(avg).strftime('%H:%M')


def _get_most_common_time(times):
  """ Gets and returns the most commonly occuring time in a list of times
  """
  most_common = collections.Counter(times).most_common(1)[0]
  return most_common[0].strftime('%H:%M')


def _get_top_temps(temps):
  """ Sorts a list of dictionaries containing temperatures and dates.
  Returns the top 10 temperatures, sorted by date.
  """
  top_temps = sorted(temps, key=lambda k: k['temp'], reverse=True)[:10]
  return sorted(top_temps, key=lambda k: _create_date(k['date']))


def _create_june_dates_list(unique_dates):
  june_dates = []

  for date in unique_dates:
    if _create_date(date).month == 6:
      june_dates.append(date)

  return sorted(june_dates)[:9]


def _is_valid_temps(hi_temp, low_temp):
  hi_temp_range_upper = constants.HI_TEMP + constants.HI_TEMP_RANGE
  hi_temp_range_lower = constants.HI_TEMP - constants.HI_TEMP_RANGE
  low_temp_range_upper = constants.LOW_TEMP + constants.LOW_TEMP_RANGE
  low_temp_range_lower = constants.LOW_TEMP - constants.LOW_TEMP_RANGE

  is_hi_temp = False
  is_low_temp = False

  if hi_temp_range_lower <= hi_temp <= hi_temp_range_upper:
    is_hi_temp = True

  if low_temp_range_lower <= low_temp <= low_temp_range_upper:
    is_low_temp = True

  if is_hi_temp or is_low_temp:
    return True

  return False


def _get_hi_temp_range():
  df = _get_weather_df()

  unique_dates = df.Date.unique()
  dates = _create_june_dates_list(unique_dates)

  valid_dates = []

  for date in dates:
    rows = df.loc[df['Date'] == date]

    for index, row in rows.iterrows():
      if _is_valid_temps(row['Hi Temperature'], row['Low Temperature']):
        valid_dates.append({
            'date': date,
            'hi_temp': row['Hi Temperature'],
            'low_temp': row['Low Temperature'],
            'time': row['Time'],
        })

  return valid_dates


def _get_average_june_temp(dates):
  """ Gets and returns the average temperature for the first
  9 days in June
  """
  df = _get_weather_df()
  temps = {date: [] for date in dates}

  for date in dates:
    rows = df.loc[df['Date'] == date]
    for index, row in rows.iterrows():
      temps[date].append(row['Outside Temperature'])

  avg_temps = {}
  for k, v in temps.items():
    avg_temps[k] = _calculate_average(v)

  return avg_temps


def _get_june_temperature_diffs():
  """ Calculates and returns the difference between the average and time's temps
  """
  df = _get_weather_df()

  unique_dates = df.Date.unique()
  dates = _create_june_dates_list(unique_dates)
  avg_temps = _get_average_june_temp(dates)

  diffs = {date: [] for date in dates}

  for date in dates:
    rows = df.loc[df['Date'] == date]
    for index, row in rows.iterrows():
      diffs[date].append({
          'diff': row['Outside Temperature'] - avg_temps[date],
          'time': row['Time'],
      })

  return diffs


def _calculate_forecast():
  diffs = _get_june_temperature_diffs()
  forecast_dates = ['0{}/07/2006'.format(i) for i in range(9)]

  forecast = {date: [] for date in forecast_dates}

  for index, (k, v) in enumerate(diffs.items()):
    for value in v:
      forecast[forecast_dates[index]].append({
          value['time']:
              '{0:.2f}'.format(constants.JULY_AVG_TEMP + value['diff'])
      })

  return forecast
