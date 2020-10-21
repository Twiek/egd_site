
from __future__ import unicode_literals
import frappe
from frappe import _


def get_home_page(user:str=""):
	return "index"


def context_extend(context):
	languages = frappe.get_hooks("translated_languages_for_website")

	context["lang"] = frappe.local.lang
	context["languages"] = languages
	context["url_lang"] = "" if frappe.local.lang == languages[0] else "/{0}".format(frappe.local.lang)

	path = frappe.local.request.path

	# Below context not needed for JS/CSS
	if not path.endswith((".js", ".css")):

		path_without_language = path
		if path == "/":
			path_without_language = ""
		elif len(path) >= 3 and path[1:3] in languages:
			path_without_language = path[3:]

		context["languages_meta"] = []
		for language in languages:
			# Main language: "x-default"
			if language == languages[0]:
				meta_url = "{0}".format(path_without_language)
			else:
				meta_url = "/{0}{1}".format(language, path_without_language)
			context["languages_meta"].append({
				"code": language,
				"hreflang": "x-default" if language == languages[0] else language,
				"url": frappe.utils.get_url(meta_url),
				"is_home": not path_without_language,
			})

		if not "context" in frappe.local.response:
			frappe.local.response.context = {}

	return context


@frappe.whitelist(allow_guest=True)
def subscribe(email):
	from frappe.utils.verified_command import get_signed_params

	url = "{0}?{1}".format(
		frappe.utils.get_url("/api/method/egd_site.tools.confirm_subscription"),
		get_signed_params({"email": email, "_lang": frappe.local.lang})
	)
	messages = (
		_("email:newsletter:body:thank_you"),
		_("email:newsletter:body:verify_your_email"),
		url,
		_("email:newsletter:body:click_here_to_verify")
	)
	content = "<p>{0}{1}</p><p><a href=\"{2}\">{3}</a></p>".format(*messages)
	frappe.sendmail(email, subject=_("email:newsletter:subject"), content=content)


@frappe.whitelist(allow_guest=True)
def confirm_subscription(email):
	from frappe.utils.verified_command import verify_request
	if not verify_request():
		return

	# Default user message
	message = frappe._dict({
		"title": _("message:title:newsletter_subscription"),
		"html": _('message:body:error_adding_email_"{0}".').format(email),
		"primary_label": _("message:body:go_to_homepage"),
	})

	group_name = "EGD Subscriptions"
	if not frappe.db.exists("Email Group", group_name):
		frappe.get_doc({
			"doctype": "Email Group",
			"title": group_name,
		}).insert(ignore_permissions=True)

	from frappe.sessions import get_geo_from_ip
	country_code = ""
	if frappe.local.request_ip:
		geo = get_geo_from_ip(frappe.local.request_ip)
		if geo and "country" in geo:
			country_code = geo["country"]["iso_code"]

	from frappe.utils import validate_email_address
	email = email.strip()
	email_valid = validate_email_address(email, False)
	if email_valid:
		if not frappe.db.get_value("Email Group Member",
			{"email_group": group_name, "email": email_valid}):
			frappe.get_doc({
				"doctype": "Email Group Member",
				"email_group": group_name,
				"email": email_valid,
				"country": country_code,
				"ip": frappe.local.request_ip,
			}).insert(ignore_permissions=True)
			frappe.get_doc("Email Group", group_name).update_total_subscribers()
			frappe.db.commit()
			message.html=_('message:body:email_"{0}"_subscribed_ok').format(email)
		else:
			message.html =_('message:body:email_"{0}"_subscribed_previously').format(email)

	frappe.respond_as_web_page(**message)


@frappe.whitelist(allow_guest=True)
def contact(email, full_name, country_code, subject, message):
	doc = frappe.get_doc({
		"doctype": "Web Contact",
		"email": email,
		"full_name": full_name,
		"country_code": country_code,
		"subject": subject,
		"message": message,
		"language": frappe.local.lang,
	})
	doc.insert(ignore_permissions=True)
	return "success"


@frappe.whitelist(allow_guest=True)
def registration(firstname, lastname, email, country_code, occupation, organization, title, donation: int, familiarity:int):
	doc = frappe.get_doc({
		"doctype": "Web Registration",
		"email": email,
		"firstname": firstname,
		"lastname": lastname,
		"country_code": country_code,
		"occupation": occupation,
		"organization": organization,
		"title": title,
		"donation": int(donation),
		"familiarity": int(familiarity),
		"language": frappe.local.lang,
	})
	doc.insert(ignore_permissions=True)
	return "success"
