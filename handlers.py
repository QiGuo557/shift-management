#!/usr/bin/env python

import webapp2
import os
import json

from google.appengine.ext.webapp import template
from models import time_interval_to_dict, update_availability


def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError


class AddAvailabilityHandler(webapp2.RequestHandler):

    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/available-time.html')

        template_values = {
            "time_interval": json.dumps(time_interval_to_dict('Qi', 1))
        }
        self.response.write(template.render(path, template_values))

    def post(self):
        time_intervals = json.loads(self.request.get('time_interval_list'))
        month = int(self.request.get('month'))
        update_availability('Qi', month, time_intervals)

        template_values = time_interval_to_dict('Qi', int(month))

        self.response.write(json.dumps(template_values))


