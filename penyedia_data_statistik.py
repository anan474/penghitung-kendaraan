
import threading

from flask import Flask
from flask_classful import FlaskView


class QuotesView(FlaskView):
    def __init__(self):
        self.quotes = [
            "A noble spirit embiggens the smallest man! ~ Jebediah Springfield",
            "If there is a way to do it better... find it. ~ Thomas Edison",
            "No one knows what he can do till he tries. ~ Publilius Syrus"
        ]

    def index(self):
        return "<br>".join(self.quotes)


class PenyediaDataStatistik():
    def __init__(self):
        self.app = Flask(__name__)

    def start(self):
        quotesview = QuotesView()
        QuotesView.register(self.app)
        self.app.run()
