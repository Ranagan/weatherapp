import datetime

from django.test import TestCase

from weatherapp.core import services

# Create your tests here.
class AverageTestCase(TestCase):
  def setUp(self):
    self.arr = [2, 4, 6]
    # (4 + 5 + 8 + 9 + 10) / 5 = 7.2
    self.arr_2 = [4, 5, 8, 9, 10]

  def test_calculate_average(self):
    test_avg = services._calculate_average(self.arr)
    test_avg_2 = services._calculate_average(self.arr_2)
    self.assertEqual(test_avg, 4)
    self.assertEqual(test_avg_2, 7.2)


class AverageTimeTestCase(TestCase):
  def setUp(self):
    time_arr = ["14:00", "15:00", "16:00"]
    time_arr_2 = ["14:00", "14:30", "13:00", "13:30"]
    self.arr = [datetime.datetime.strptime(time, '%H:%M') for time in time_arr]
    self.arr_2 = [datetime.datetime.strptime(time, '%H:%M') for time in time_arr_2]

  def test_average_time(self):
    test_avg = services._get_average_time(self.arr)
    test_avg_2 = services._get_average_time(self.arr_2)
    self.assertEqual(test_avg, "15:00")
    self.assertEqual(test_avg_2, "13:45")


class MostCommonTimeTestCase(TestCase):
  def setUp(self):
    arr = ["12:00", "12:00", "12:00", "13:45", "13:45", "10:15"]
    arr_2 = ["12:00", "13:00", "12:00", "23:50", "23:50", "13:00"]
    self.arr = [datetime.datetime.strptime(time, '%H:%M') for time in arr]
    self.arr_2 = [datetime.datetime.strptime(time, '%H:%M') for time in arr_2]

  def test_most_common_times(self):
    most_common = services._get_most_common_time(self.arr)
    most_common_2 = services._get_most_common_time(self.arr_2)
    self.assertEqual(most_common, "12:00")
    # Returns first in array if same count
    self.assertEqual(most_common_2, "12:00")


class JuneDatesTestCase(TestCase):
  def setUp(self):
    self.arr = ["12/12/2006", "01/06/2006", "02/06/2006", "13/01/2006"]
    # To make sure it's sorting
    self.arr_2 = ["12/12/2006",  "02/06/2006", "01/06/2006", "13/01/2006"]

  def test_get_june_dates(self):
    june_dates = services._create_june_dates_list(self.arr)
    june_dates_2 = services._create_june_dates_list(self.arr_2)
    self.assertEqual(june_dates, ["01/06/2006", "02/06/2006"])
    self.assertEqual(june_dates_2, ["01/06/2006", "02/06/2006"])


class IsValidTempTestCase(TestCase):
  def setUp(self):
    self.temp = 22.5
    self.temp_2 = 23.4
    self.temp_3 = 10.5
    self.temp_4 = 10.6

  def test_is_valid_temp(self):
    # One valid
    self.assertEqual(services._is_valid_temps(self.temp, self.temp_2), True)
    # Both valid
    self.assertEqual(services._is_valid_temps(self.temp, self.temp_3), True)
    # None valid
    self.assertEqual(services._is_valid_temps(self.temp_2, self.temp_4), False)
