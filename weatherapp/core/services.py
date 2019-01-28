import collections
import datetime
import io

from weatherapp.core import constants

import requests
import pandas



def get_weather_data():
  """ Fetches the weather data CSV from the given URL

  """
  response = requests.get(constants.WEATHER_CSV_URL)
  data = response.content.decode('utf-8')

  df = pandas.read_csv(
      io.StringIO(data), usecols=constants.WEATHER_CSV_FIELDNAMES)

  return df


def format_date(date_str):
  return datetime.datetime.strptime(date_str, '%d/%m/%Y')


def get_highest_temps():
  """ Creates a dictionary of the highest temperatures
  """
  df = get_weather_data()
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


def get_average_time(times):
  """ Calculates and returns the average time in a list of times
  """
  total = sum(dt.hour * 3600 + dt.minute * 60 + dt.second for dt in times)
  avg = total / len(times)

  return datetime.datetime.fromtimestamp(avg).strftime('%H:%M')


def get_most_common_time(times):
  """ Gets and returns the most commonly occuring time in a list of times
  """
  most_common = collections.Counter(times).most_common(1)[0]
  return most_common[0].strftime('%H:%M')


def get_top_temps(temps):
  top_temps = sorted(temps, key=lambda k: k['temp'], reverse=True)[:10]
  return sorted(top_temps, key=lambda k: format_date(k['date']))


def get_outside_temp_context():
  highs = get_highest_temps()
  times = []
  temps = []
  for value in highs.values():
    times.append(datetime.datetime.strptime(value['time'], '%H:%M'))

  for k, v in highs.items():
    temps.append({'date': k, 'temp': v['temp']})

  avg_time = get_average_time(times)
  most_common = get_most_common_time(times)
  top_temps = get_top_temps(temps)

  return {
      'time': avg_time,
      'most_common_time': most_common,
      'top_temps': top_temps,
  }
