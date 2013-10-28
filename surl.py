import os, tempfile, urlparse, weechat, re, urllib

weechat.register( "sURL", "backtick", "1.0", "GPL", "Waits for URLs and writes redirector html files somewhere", "", "" )

surlParams = ("urllength", "prefix", "suffix", "directory")

if weechat.config_get_plugin('urllength') == "":
	weechat.config_set_plugin('urllength', "30")

weechat.hook_signal("*,irc_in2_privmsg", "surl_handle_message", "")
weechat.hook_command("surl", "Sets/gets sURL settings.", "urllength|activechans|printall|directory", \
	"[<variable> [[=] <value>]]",
"""When run without arguments, displays all sURL settings

<variable> : Sets or displays a single sURL setting. One of:
	urllength [[=] length]
		Minimal length of URLs that will be shortened.
		Default: 30
	prefix [[=] url]
		Prefix for URL ids to form a full URL.
		Default: None
	suffix [[=] suffix]
		Suffix to give redirector file. .htm and .html are useful.
		Default: None
	directory [[=] dir]
		Directory shortened URLs will be dropped into as HTML redirectors.
		Default: None""",
	"surl_main", "")
	
def get_var(name = None):
	target = weechat.buffer_search("", "")
	weechat.prnt(target, "-sURL- Configuration:")
	if name != None and not name in surlParams:
		weechat.prnt(target, "\tUnknown parameter \"%s\", try '/help surl'" % name)
		return
	keys = [name] if name != None else surlParams
	for name in keys:
		weechat.prnt(target, "\t%s = %s" % (name, weechat.config_get_plugin(name)))

def set_var(name, value):
	target = weechat.buffer_search("", "")
	weechat.prnt(target, "-sURL- Configuration:")
	if name not in surlParams:
		weechat.prnt(target, "\tUnknown parameter \"%s\", try '/help surl'" % name)
		return

	if name == "urllength":
		try:
			v = int(value)
			if v < 1:
				weechat.prnt(target, "\turllength must be at least 1")
				return
		except:
			weechat.prnt(target, "\turrlength must be integral")
			return

	weechat.config_set_plugin(name, value)
	weechat.prnt(target, "\t%s = %s" % (name, weechat.config_get_plugin(name)))

def make_redirect(url, target):
	template = """<!DOCTYPE html>
<html>
	<head>
		<title>Redirect</title>
		<meta http-equiv="refresh" content="0; url=%s" />
	</head>
	<body>
		Click <a href="%s">here</a> to proceed
	</body>
</html>
"""
	url = urllib.quote(url)
	dir = weechat.config_get_plugin("directory")
	try:
		id = 0
		last_file = os.path.join(dir, ".last")
		if os.path.isfile(last_file):
			with open(last_file) as last:
				id = int(last.readline(30).strip())
		id = id + 1
		with open(last_file, "w+") as last:
			last.write(str(id))
		redir_name = str(id) + weechat.config_get_plugin("suffix")
		with open(os.path.join(dir, redir_name), "w+") as redirector:
			redirector.write(template % (url, url))
		weechat.prnt(target, "[AKA] %s/%s" % (weechat.config_get_plugin("prefix"), redir_name))
	except:
		weechat.prnt(target, "[sURL] Could not create file")

def clean_url(url):
	safe = "$-_.+!*'(),%:@&=?/;#"
	for i in range(len(url)):
		if not url[i].isalnum() and url[i] not in safe:
			return url[:i]
	return url

def surl_handle_message(data, signal, signal_data):
	(server, sig) = signal.split(",", 1)
	maxlen = int(weechat.config_get_plugin("urllength"))
	(source, type, channel, msg) = signal_data.split(" ", 3)
	if not channel.startswith("#"):
		channel = source.split("!", 2)[0][1:]

	buffer = weechat.buffer_search("", server + "." + channel)

	msg = msg[1:]
	
	words = msg.split()
	for word in words:
		word = clean_url(word)
		url = urlparse.urlparse(word)
		if url.scheme != "" and len(word) > maxlen:
			make_redirect(word, buffer)
	return weechat.WEECHAT_RC_OK

def surl_main(data, buffer, args):
	args = args.split(" ")
	while '' in args:
		args.remove('')
	while ' ' in args:
		args.remove(' ')

	if len(args) < 2:
		get_var(args[0] if len(args) > 0 else None)
	else:
		name = args[0]
		value = ""
		if args[1] == "=":
			value = " ".join(args[2:])
		else:
			value = " ".join(args[1:])
		set_var(name, value)
	return weechat.WEECHAT_RC_OK
