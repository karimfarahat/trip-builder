import requests
def send_simple_message(key, message):
	return requests.post(
		"https://api.mailgun.net/v3/sandbox6205489a424a4f3297b14975e1f85a5b.mailgun.org/messages",
		auth=("api", key),
		data={"from": "Mailgun Sandbox <postmaster@sandbox6205489a424a4f3297b14975e1f85a5b.mailgun.org>",
			"to": "Karim Farahat <karim.f.farahat@pwc.com>",
			"subject": "Hello Karim Farahat",
			"text": message})

# You can see a record of this email in your logs: https://app.mailgun.com/app/logs.

# You can send up to 300 emails/day from this sandbox server.
# Next, you should add your own domain so you can send 10000 emails/month for free.