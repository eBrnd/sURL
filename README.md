sURL
====

**Really simple URL shortener for weechat**


Problem
-------

You have weechat running in a text console, probably using screen on a remote machine.
Someone pastes a really long link in a channel, far longer than a line in your terminal window.
It's not trivial to get that link into your web browser, sometimes it involves resizing the window and selecting the link manually.

There are already some plugins that handle that problem, e.g. by launching a web browser command directly (not that useful when you're running weechat on a vserver...) or by using a 3rd party URL shortener.
Both these solutions are not too pleasing, so here's a new one:


New Solution
------------

*Why not just use the web server that's running on my vserver anyway to serve the shortened URLs?*

Here's how it works:

You need a webserver, and weechat, and some folder that can be written to by weechat, and read by the webserver (that can even be a network share or something).
When weechat sees a (long) link in a channel, it creates an HTML file in that folder.
This file has a really short name, and contains just a redirect to the original long link.

The new, short link, is added to the buffer after the original long link.
Now you can just click, or copypaste the short link into your browser.


Installation
------------

Just dump `surl.py` into your `.weechat/python` or `.weechat/python/autoload` folder, and type `/python load surl.py` to start it up.


Configuration
-------------

sURL's config options can be found using `/set plugins.var.python.surl.*`.

* `directory`: The directory the HTML files are placed in. This should be some directory that is shared by your webserver. *Make sure you (the user weechat is running as) can write to that directory!*
* `prefix`: The prefix of the short link. You need to set this to wherever your webserver is serving the `directory`.
* `suffix`: File name suffix. Most commonly `.html`, but you can make your own, like `-my-short-link.htm` or something.
* `urllength`: URL length threshold that triggers sURL. If a link is shorter than this, we won't even bother shortening it.


Usage
-----

Just wait for someone to post a link in a channel or query.
You'll see the original link, followed by `[AKA]` and the shortened link.
If you webserver is setup correctly, clicking that link should take you to the originally posted URL.
