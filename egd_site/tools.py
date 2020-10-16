
from __future__ import unicode_literals
import frappe
from frappe import _


def get_home_page(user:str=""):
	return "index"


def context_extend(context):
	# CONTEXT: check order in "def build_context(context):"

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
	from frappe.sessions import get_geo_ip_country

	country = get_geo_ip_country(frappe.local.request_ip) if frappe.local.request_ip else None,

	url = "{0}?{1}".format(
		frappe.utils.get_url("/api/method/egd_site.tools.confirm_subscription"),
		get_signed_params({"email": email})
	)
	messages = (
		_("Thank you for subscribing to our updates."),
		_("Please verify your email address:") + country,
		url,
		_("Click here to verify")
	)
	content = """
	<p>{0}{1}</p>
	<p><a href="{2}">{3}</a></p>
	"""
	frappe.sendmail(email, subject=_("Confirm your email"), content=content.format(*messages))


@frappe.whitelist(allow_guest=True)
def confirm_subscription(email):
	from frappe.utils.verified_command import verify_request

	if not verify_request():
		return

	group_name = "EGD Subscriptions"
	if not frappe.db.exists("Email Group", group_name):
		frappe.get_doc({
			"doctype": "Email Group",
			"title": group_name,
		}).insert(ignore_permissions=True)

	from frappe.email.doctype.email_group.email_group import add_subscribers
	frappe.flags.ignore_permissions = True
	add_subscribers(group_name, email)
	frappe.db.commit()

	frappe.respond_as_web_page(_("Confirmed"),
		_("{0} has been successfully added to the Email Group.").format(email),
		indicator_color='green')
