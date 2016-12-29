from google.appengine.ext import ndb


class Availability(ndb.Model):
    employee = ndb.StringProperty(required=True, default='Qi')
    month = ndb.IntegerProperty(required=True)
    date = ndb.DateProperty(required=True)
    start_time = ndb.TimeProperty(required=True)
    end_time = ndb.TimeProperty(required=True)


def save_availability(month, date, start_time, end_time):
    availability = Availability(month=month, date=date, start_time=start_time, end_time=end_time)
    availability.put()
    return availability


