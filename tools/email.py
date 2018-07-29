import re
from html import unescape
import urlextract

url_extractor = urlextract.URLExtract()


def html_to_plain_text(html):

	replacement_list = [
		(r"<head.*?>.*?</head>", ""),
		(r"<a\s.*?>", " HYPERLINK "),
		(r"<.*?>", ""),
		(r"(\s*\n)+", "\n"),
	]

	for (pattern, replacement) in replacement_list:
		html = re.sub(pattern, replacement, html, flags=re.S | re.I)

	return unescape(html)


def email_to_text(email, unify_urls=True, unify_numbers=True):

	try:
		from_ = email.get("from")
	except IndexError:
		from_ = None

	domain = re.search("@(.+)", from_) if from_ else None

	try:
		subject = email.get("subject")
	except IndexError:
		subject = None

	content = "{} {} {} ".format(
		from_ if from_ else "EMPTYFROM",
		domain if domain else "EMPTYDOMAIN",
		subject if subject else "EMPTYSUBJECT"
	)

	is_html = False

	for part in email.walk():
		content_type = part.get_content_type()

		if content_type not in ("text/plain", "text/html"):
			continue

		try:
			content += part.get_content()
		except:
			content += str(part.get_payload())

		if content_type == "text/html":
			is_html = True

		break

	content = content.strip()

	if not content:
		return ""

	if is_html:
		content = html_to_plain_text(content)

	if unify_numbers:
		content = re.sub(r"[\d][\d.]*", " NUMBER ", content)

	if unify_urls:
		urls = list(set(url_extractor.find_urls(content)))
		urls.sort(key=lambda url: len(url), reverse=True)
		for url in urls:
			content = content.replace(url, " URL ")

	return str(content)
