#!/usr/bin/python
# need to fix the date extraction IMPORTANT
import urllib2
import re
import datetime

NOTICE_URL = 'http://tp.iitkgp.ernet.in/notice/index.php?page=1'

NOTICE_BEGIN_PATTERN = 'return false">(\s*)(?=\w)'
NOTICE_END_PATTERN = '</a></td></tr><tr>'
DATE_BEGIN_PATTERN = '<font class=text>'
DATE_END_PATTERN = ''


def get_today():
    date_string=""
    today = datetime.date.today()
    if today.day/10 == 0:
        date_string = "0"+str(today.day)
    else:
        date_string = str(today.day)

    if today.month==1:
    	month="Jan"
    elif today.month==2:
        month="Feb"
    elif today.month==3:
        month="Mar"
    elif today.month==4:
        month="Apr"
    elif today.month==5:
        month="May"
    elif today.month==6:
        month="Jun"
    elif today.month==7:
    	month="Jul"
    elif today.month==8:
        month="Aug"
    elif today.month==9:
        month="Sep"
    elif today.month==10:
        month="Oct"
    elif today.month==11:
        month="Nov"
    elif today.month==12:
        month="Dec"

    date_string += " "+month
    return date_string

def getDate(line):
    first = re.search(DATE_BEGIN_PATTERN ,line)
    if first :
        first = first.end()
        return line[first : first+17]
    else :
        return ""

def getNotice(line):
    first = re.search(NOTICE_BEGIN_PATTERN,line)
    second = re.search(NOTICE_END_PATTERN,line)
    if first and second :
        return line[first.end() : second.start()]
    else :
        return ""

def latest_notice(source):
    notice = getNotice(source)
    date = getDate(source)
    if notice == "" or date == "":
        return ""
    return date +"\t\t" +notice+"\n"

def all_notices(source):
    notices=""
    while 1:
        notice = latest_notice(source)
        if notice == "":
            break
        notices += notice

        t = re.search(NOTICE_END_PATTERN , source).end()
        source = source[t:]
    return notices

def today_notices(source):
    today = get_today()
    notices=""
    while 1:
        notice = getNotice(source)
        date = getDate(source)
        if notice == "" or date == "":
            break
        if date[0:6]==today:
            notices += date + "\t\t" + notice + "\n"

        t = re.search(NOTICE_END_PATTERN , source).end()
        source = source[t:]
    return notices

if __name__ == '__main__' :
    print "Getting http request.."
    usock = urllib2.urlopen(NOTICE_URL)
     
    print "Reading page..\n"
    page_source = usock.read()

    #print "ALL NOTICES\n"+all_notices(page_source)
    print "LATEST NOTICE\n"+latest_notice(page_source)
    #print "TODAY'S NOTICES\n"+today_notices(page_source)

    usock.close()
    print "Http Connnection closed!!"



