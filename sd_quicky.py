import gdata
from gdata.calendar import client, data
from bottle import route, run, debug, template, request, validate, error, response, redirect
import re
from datetime import date, timedelta, datetime
import bitly
import feed.date.rfc3339

BITLY_LOGIN="sdbaltimore"
BITLY_API="R_3677d6826fab742f02f027226dff3d2c"
BITLY=bitly.Api(login=BITLY_LOGIN,apikey=BITLY_API)

def parseEntry(entry):
    d={}
    d["title"]=entry.title.text
    date=entry.when.pop(0)
    timestamp_start = datetime.fromtimestamp(feed.date.rfc3339.tf_from_timestamp(date.start))
    timestamp_end = datetime.fromtimestamp(feed.date.rfc3339.tf_from_timestamp(date.end))
    d["when"]= timestamp_start.strftime('%A, %B %d from %I:%M %p') + timestamp_end.strftime(' to %I:%M %p')
    d["where"]=entry.where.pop(0).value
    content=entry.content.text
    if content is None:
        content = "Blank SOOOONNNN!"
    d["description"]=content
    link_regex = re.findall("http://[^ \s]+|www.[^ \s]+",content)
    if link_regex is None:
        d["short-link"] = "No Link"
    else:
        d["short-link"] = []
      
    for link in link_regex:
        # If link is already a bitly link ...
        if re.match("http://bit.ly/[^ \s]+", link):
            # Turn it back into a long form URL ...
            newBitly = BITLY.expand(link)
            # Then shorten it again with our account so we can track it.
            d["short-link"].append(BITLY.shorten(newBitly))
        else:
            d["short-link"].append(BITLY.shorten(link))
    return d

def monday2monday(near):
    #gcal api uses inclusive start date, exclusive end date
    #find the nearest monday => isoweekday 1
    one_day=timedelta(days=1)
    while near.isoweekday() != 1:
        near=near+one_day
    #find the following one
    following_sunday=near+(7*one_day)
    return (near.strftime('%Y-%m-%d'),following_sunday.strftime('%Y-%m-%d'))

def printAllLinks(list):
    for link in list:
        print 'More info: <a href="%s">%s</a>'


@route('/')
def redirect_to_closest_feed():
    closestWeek=monday2monday(date.today())
    redirect('/feed/%s/%s'%(closestWeek))

@route('/feed/:start/:end')
def show_feed(start,end):
    #we got the feed
    calendar_client = gdata.calendar.client.CalendarClient()
    feed_uri="https://www.google.com/calendar/feeds/l4ut8vep3q5ammqv91n205u3lc%40group.calendar.google.com/private-75b3611bd28055ede485cb6afd9380b9/full?orderby=starttime&sortorder=ascending"

    #for time
    query = gdata.calendar.client.CalendarEventQuery()
    query.start_min = start  #start_date "2007-06-26"
    query.start_max = end    #end_date "2007-07-01"

    feed = map(parseEntry,calendar_client.GetCalendarEventFeed(uri=feed_uri,q=query).entry)

    #find out next/prev week start/end
    week_start=datetime.strptime(start, '%Y-%m-%d')
    nextweek=monday2monday(week_start+timedelta(days=7))
    lastweek=monday2monday(week_start-timedelta(days=7))

    return template("feed.tpl",locals())

# Would be cool if we could pass feed_uri in the URL so that we could test other cals and let people use our fun tool.
@route('/othercal/:feed_uri/:start/:end')
def show_feed(feed_uri,start,end):
    #we got the feed
    calendar_client = gdata.calendar.client.CalendarClient()

    #for time
    query = gdata.calendar.client.CalendarEventQuery()
    query.start_min = start  #start_date "2007-06-26"
    query.start_max = end    #end_date "2007-07-01"

    feed = map(parseEntry,calendar_client.GetCalendarEventFeed(uri=feed_uri,q=query).entry)

    #find out next/prev week start/end
    week_start=datetime.strptime(start, '%Y-%m-%d')
    nextweek=monday2monday(week_start+timedelta(days=7))
    lastweek=monday2monday(week_start-timedelta(days=7))

    return template("feed.tpl",locals())

if __name__ =="__main__":
    debug(True)
    run(reloader=True)
