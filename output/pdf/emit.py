#!/usr/bin/env python3

import datetime
import random
import pymongo as mongo

from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Spacer, ListFlowable, ListItem, KeepTogether
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle, ListStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

from custom_flowables import TimelineItem

title_style = ParagraphStyle("title", alignment=TA_CENTER, fontSize=18, spaceAfter=10)
subtitle_style = ParagraphStyle("subtitle", alignment=TA_CENTER, fontSize=14, spaceBefore=24, spaceAfter=10)
plain_para_style = ParagraphStyle("plain_para", spaceBefore=10, spaceAfter=10)
list_item_style = ListStyle("list_item")


class Street(object):
    """A range of street, closed because of an event."""
    def __init__(self):
        super(Street, self).__init__()
        self.street_name = "Corrine St."

    def __str__(self):
        return self.street_name

example_people = [(t, t.lower()+"@example.com") for t in "Alice Bill Carol Dave Elise Fred Giselle Harry Irene".split()]

class Event(object):
    """A collection of streets, and a range of time, and a name."""
    def __init__(self):
        super(Event, self).__init__()
        self.title = "Example Event 2015"
        self.streets = Street(), Street(), Street()
        self.closed_periods = [(datetime.datetime.utcnow() - datetime.timedelta(hours=random.randint(24, 36)), datetime.datetime.utcnow() - datetime.timedelta(hours=random.randint(-5, 25)))]
        self.contact_name, self.contact_email = random.choice(example_people)
        self.contact_phone = "+1 407-555-1823"
        self.see_also_web = "http://parade.example.com/orlando/2016"
        self.timeline = None

    def details_as_flowable(self):
        return Paragraph(self.title + ", Contact: " + self.contact_name + "<" + self.contact_email + ">,\nclosed: " + ",\n".join(str(s) for s in self.streets), plain_para_style)

    def summary_as_flowable(self):
        return ListItem(Paragraph(self.title, plain_para_style), list_item_style)

    def set_timeline(self, timeline):
        self.timeline = timeline

    def timeline_as_flowable(self):
        return self.timeline

def get_timeline_data(events):
    time_line_min, time_line_max = None, None
    for event in events:
        for start_time, end_time in event.closed_periods:
            assert start_time < end_time
            time_line_min = min(time_line_min, start_time) if time_line_min else start_time
            time_line_max = max(time_line_max, end_time) if time_line_max else end_time

    result = list()  # tuple of (event, list of (0-1 start position, 0-1 end position, start_time, end_time)) .
    time_line_duration = time_line_max - time_line_min   # timedelta
    time_line_duration_seconds = time_line_duration.total_seconds()
    for event in events:
        periods = list()
        for start_time, end_time in event.closed_periods:
            
            start_time_delta = start_time - time_line_min
            end_time_delta = end_time - time_line_min
            periods.append((start_time_delta.total_seconds()/time_line_duration_seconds,  end_time_delta.total_seconds()/time_line_duration_seconds, start_time, end_time))
        result.append((event, periods))
    return result


def get_events(start_time, stop_time):
    return [Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event()]


def insert_title(story, starting_date, ending_date, title="Road Closure Status Report"):
    if ending_date and ending_date.date() != starting_date.date():
        subtitle = starting_date.strftime("%-d %B %Y") + " — " + ending_date.strftime("%-d %B %Y")
    else:
        subtitle = starting_date.strftime("%-d %B %Y")

    story.append(Paragraph(title, title_style))
    story.append(Paragraph(subtitle, subtitle_style))
    story.append(Spacer(0, 0.5 * inch))


def insert_events(story, events, with_summary=False):
    details = list()
    summary = list()
    for event in events:
        tl = event.timeline_as_flowable()
        if tl:
            details.append(KeepTogether([event.details_as_flowable(), tl]))
        else:
            details.append(event.details_as_flowable())
        summary.append(event.summary_as_flowable())

    if with_summary:
        story.append(Paragraph("{0} items:".format(len(events)), plain_para_style))
        story.append(ListFlowable(summary, bulletType="bullet"))
        story.append(PageBreak())

    story.extend(details)


def generate(output_file, starting_date, ending_date=None):
    if not ending_date:
        ending_date = datetime.datetime.utcnow()
    events = get_events(starting_date, ending_date)
    events.sort(key=lambda e: e.title)
    timeline_data = get_timeline_data(events)

    for event, periods in timeline_data:
        print(event.title)
        for period in periods:
            print(" "*int(80*period[0]), "#"*int(80*(period[1]-period[0])))
        print()


    story = list()
    try:
        insert_title(story, starting_date, ending_date)
        for event, periods in timeline_data:
            event.set_timeline(TimelineItem(event.title, periods))
        insert_events(story, events, with_summary=len(events) > 20)
    finally:
        doc = SimpleDocTemplate(output_file)
        doc.multiBuild(story)

    return output_file


if __name__ == "__main__":
    with open("test.pdf", "wb") as out:
        generate(out, datetime.datetime.utcnow() - datetime.timedelta(days=2))
