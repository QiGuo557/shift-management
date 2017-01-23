#!/usr/bin/env python

import handlers
import webapp2


app = webapp2.WSGIApplication([
    ('/', handlers.AddAvailabilityHandler),
], debug=True)
