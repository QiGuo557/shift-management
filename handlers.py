#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
from datetime import datetime
from google.appengine.ext.webapp import template
from models import initialize_availability, insert_availability, retrieve_availability


class AddAvailabilityHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'templates/available-time.html')
        self.response.write(template.render(path, template_values))

    def post(self):
        date = datetime.strptime(self.request.get('availability_date'), '%Y-%m-%d').date()
        month = date.month
        start_time = datetime.strptime(self.request.get('availability_start_time'), '%H:%M').time()
        end_time = datetime.strptime(self.request.get('availability_end_time'), '%H:%M').time()
        insert_availability(employee="Qi", month=month, date=date, start_time=start_time, end_time=end_time)
        retrieve_availability(employee="Qi", month=month)
        self.redirect('/')

