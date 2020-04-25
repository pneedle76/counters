#!/usr/bin/python

from django.http import HttpResponse
import sys, datetime, time

year = datetime.datetime.today().year

def index(request):
  while True:
    delta = datetime.datetime(year, 12, 25) - datetime.datetime.now()
    days = delta.days
    hours = int(delta.seconds / 3600)
    minutes = int((delta.seconds - (hours * 3600)) / 60)
    seconds = int(delta.seconds - (hours * 3600)) - (minutes * 60)
    return HttpResponse("There are %s days, %i hours, %s minutes and %s seconds until Christmas!\r" % (days, hours, minutes, seconds))
    time.sleep( 1 )
