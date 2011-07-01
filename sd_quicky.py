import gdata
from gdata.calendar import client
from bottle import route, run, debug, template, request, validate, error


@route('/feed/:start/:end')
def show_feed(start,end):
    #we got the feed
    calendar_client = gdata.calendar.client.CalendarClient()
    feed_uri="https://www.google.com/calendar/feeds/l4ut8vep3q5ammqv91n205u3lc%40group.calendar.google.com/private-75b3611bd28055ede485cb6afd9380b9/basic"

    #for time
    query = gdata.calendar.client.CalendarEventQuery()
    query.start_min = start  #start_date "2007-06-26"
    query.start_max = end    #end_date "2007-07-01"
    print "Start: %s" % start
    print end
    feed = calendar_client.GetCalendarEventFeed(uri=feed_uri,q=query).entry

    return template("feed.tpl",locals())

debug(True)
run(reloader=True)

#for i, an_event in enumerate(feed.entry):
#  print '\t%s. %s' % (i, an_event.title.text,)
