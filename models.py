from datetime import datetime
from google.appengine.ext import ndb


class TimeInterval(ndb.Model):
    date = ndb.DateProperty()
    start_time = ndb.TimeProperty()
    end_time = ndb.TimeProperty()

    def to_dict(self):
        time_interval_dict = {}
        time_interval_dict['date'] = self.date.isoformat()
        time_interval_dict['start_time'] = self.start_time.isoformat()
        time_interval_dict['end_time'] = self.end_time.isoformat()
        return time_interval_dict


class Availability(ndb.Model):
    employee = ndb.StringProperty(required=True, default='Qi')
    month = ndb.IntegerProperty()
    time_interval = ndb.StructuredProperty(TimeInterval, repeated=True)

    @classmethod
    def build_key(cls, key1, key2):
        key_string = u'' + str(key1) + '-' + str(key2)
        return ndb.Key(Availability, key_string)

    def set_key(self):
        self.key = self.build_key(self.employee, self.month)

    @classmethod
    def query_availability_by_key(cls, employee, month):
        availability_key = cls.build_key(employee, month)
        return cls.query(Availability.key == availability_key).order(cls.time_interval.date,
                                                                     cls.time_interval.start_time).get()


def time_interval_to_dict(employee, month):
    availability = retrieve_availability(employee, month)
    if availability:
        time_interval_list = availability.time_interval

        template_values = {
            "time_interval_list": [time_interval.to_dict() for time_interval in time_interval_list]
        }
    else:
        template_values = {
            "time_interval_list": []
        }
    return template_values


def initialize_availability(employee, month):
    availability = Availability(employee=employee, month=month)
    availability.set_key()
    availability.put()
    return availability


def insert_availability(employee, month, date, start_time, end_time):
    availability = retrieve_availability(employee, month)
    time_interval = TimeInterval(date=date, start_time=start_time, end_time=end_time)
    if not availability:
        availability = Availability(employee=employee, month=month, time_interval=[time_interval])
        availability.set_key()
    else:
        availability.time_interval.append(time_interval)
    availability.put()
    return availability


def update_availability(employee, month, time_interval_list):
    availability = retrieve_availability(employee, int(month))
    time_intervals = []

    for time_interval in time_interval_list:
        date = datetime.strptime(time_interval['date'], '%Y-%m-%d').date()
        start_time = datetime.strptime(time_interval['start_time'], '%H:%M:%S').time()
        end_time = datetime.strptime(time_interval['end_time'], '%H:%M:%S').time()
        time_intervals.append(TimeInterval(date=date, start_time=start_time, end_time=end_time))

        if not availability:
            availability = Availability(employee=employee, month=month)
            availability.set_key()

    availability.time_interval = time_intervals
    availability.put()
    return availability


def retrieve_availability(employee, month):
    return Availability.query_availability_by_key(employee, month)