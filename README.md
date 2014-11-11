# Choose Your Own Adventure Presentations
Use this code to create real-time branching presentations so 
audiences can choose the path through your next technical talk.

Detailed installation instructions and a walkthrough of the code base
can be found in 
[this blog post I wrote for Twilio](https://www.twilio.com/blog/2014/11/choose-your-own-adventure-presentations-with-reveal-js-python-and-websockets.html).


## See it in action
Here's a screenshot of the vanilla choices screen. You can of course modify
this initial screen with your own styles and visualizations.

<img src="./cyoa/static/img/cyoa-choices.jpg">

You can check out how
these branching presentations work if you watch the DjangoCon 2014 video 
"[Choose Your Own Django Deployment Adventure](https://www.youtube.com/watch?v=QrFEKghISEI)" 
with [Matt Makai](https://twitter.com/mattmakai) and 
[Kate Heddleston](https://twitter.com/heddle317). 


## Software stack
Uses 
[reveal.js](http://lab.hakim.se/reveal-js/#/), 
[Python](https://www.python.org/), 
[Flask](http://flask.pocoo.org/), 
[WebSockets](http://en.wikipedia.org/wiki/WebSocket) 
(via the amazing 
[Flask-SocketIO](https://flask-socketio.readthedocs.org/en/latest/) 
extension) and [Twilio SMS](https://www.twilio.com/sms).

Yes, we used a Flask app at DjangoCon. For shame.


## Authors
Created by [Matt Makai](http://github.com/makaimc) and 
[Kate Heddleston](https://github.com/heddle317). 
