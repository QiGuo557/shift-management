from google.appengine.ext import ndb


class TimeInterval(ndb.Model):
    date = ndb.DateProperty()
    start_time = ndb.TimeProperty()
    end_time = ndb.TimeProperty()


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
    def query_availability(cls, employee, month):
        availability_key = cls.build_key(employee, month)
        return cls.query(Availability.key == availability_key).get()


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


def retrieve_availability(employee, month):
    return Availability.query_availability(employee, month)
