from reportlab.platypus.flowables import Flowable
from reportlab.lib.colors import orangered, gray
from reportlab.lib.units import inch


class TimelineItem(Flowable):
    def __init__(self, event_name, closures):
        self.event_name = event_name
        self.closures = closures
        self.suggested_width = None

    def wrap(self, *args):
        self.suggested_width = args[0]
        return 0, inch*0.75

    def draw(self):
        canvas = self.canv
        for closure in self.closures:
            path = canvas.beginPath()
            path.moveTo(closure[0]*self.suggested_width, inch*0.75)
            path.lineTo(closure[0]*self.suggested_width, inch*(0.5+0.1))
            canvas.setLineWidth(1)
            canvas.setStrokeColor(gray)
            canvas.drawPath(path)

            path = canvas.beginPath()
            path.moveTo(closure[1]*self.suggested_width, inch*0.75)
            path.lineTo(closure[1]*self.suggested_width, inch*(0.25+0.1))
            canvas.drawPath(path)

            path = canvas.beginPath()
            path.moveTo(closure[0]*self.suggested_width, inch*0.75)
            path.lineTo(closure[1]*self.suggested_width, inch*0.75)
            canvas.setStrokeColor(orangered)
            canvas.setLineWidth(6)
            canvas.drawPath(path)

            full_date_format = "%H:%M, %-d %B %Y"
            date_format = full_date_format
            if closure[2].date() == closure[3].date():
                date_format = "%H:%M"
            canvas.drawString(closure[0]*self.suggested_width, inch*0.5, closure[2].strftime(full_date_format))
            canvas.drawRightString(closure[1]*self.suggested_width, inch*0.25, closure[3].strftime(date_format))
