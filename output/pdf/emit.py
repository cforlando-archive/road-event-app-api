#!/usr/bin/env python3

import datetime
import pymongo as mongo

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import SimpleDocTemplate, Frame, Paragraph, PageBreak, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import ParagraphStyle, ListStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

title_style = ParagraphStyle("title", alignment=TA_CENTER, fontSize=18, spaceAfter=10)
subtitle_style = ParagraphStyle("subtitle", alignment=TA_CENTER, fontSize=14, spaceBefore=24, spaceAfter=10)
plain_para_style = ParagraphStyle("plain_para", spaceBefore=10, spaceAfter=10)
list_item_style = ListStyle("list_item")


class Street(object):
    """A range of street, closed because of an event."""
    def __init__(self):
        super(Street, self).__init__()
        self.street_name = "Main"

    def __str__(self):
        return self.street_name

class Event(object):
    """A collection of streets, and a range of time, and a name."""
    def __init__(self):
        super(Event, self).__init__()
        self.title = "sample title"
        self.streets = Street(), Street(), Street()
        self.start_time = "starttime"
        self.end_time = "endtime"
        self.contact_name = "Alice"
        self.contact_email = "alice@example.com"
        self.contact_phone = "+1 407-555-1823"
        self.see_also_web = "http://parade.example.com/orlando/2016"

    def details_as_flowable(self):
        return Paragraph(self.title + "\n" + self.start_time + "\n" + self.contact_name + "\n" + "\n".join(str(s) for s in self.streets), plain_para_style)

    def summary_as_flowable(self):
        return ListItem(Paragraph(self.title + ", " + self.start_time, plain_para_style), list_item_style)


def get_events(start_time, stop_time):
    return Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), Event(), 


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
        details.append(event.details_as_flowable())
        summary.append(event.summary_as_flowable())

    if with_summary:
        story.append(Paragraph("{0} items:".format(len(events)), plain_para_style))
        story.append(ListFlowable(summary, bulletType="bullet"))
        story.append(PageBreak())

    story.extend(details)


def generate(output_file, starting_date, ending_date=None):
    if not ending_date:
        ending_date = datetime.datetime.now()
    events = get_events(starting_date, ending_date)
    story = list()
    try:
        insert_title(story, starting_date, ending_date)
        insert_events(story, events, with_summary=len(events) > 9)
    finally:
        page_width, page_height = letter
        canvas = Canvas(output_file, pagesize=(page_width, page_height),)

        doc = SimpleDocTemplate(output_file)
        doc.multiBuild(story)

    return output_file


if __name__ == "__main__":
    from io import BytesIO

    with open("test.pdf", "wb") as out:
        generate(out, datetime.datetime.now() - datetime.timedelta(days=2))
