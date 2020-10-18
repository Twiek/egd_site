# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe

__version__ = '0.0.1'



def is_app_for_actual_site() -> bool:
	"""
	When overriding Frappe or other apps methods, it allow us
	to set that specific override to the actual `site app`.
	Used when multi tenancy (multisites) is on.

	:rtype: bool
	"""
	from .hooks import site_app_domains as sites
	return frappe.local.site in sites


def site_env() -> str:
	"""
	Get actual site environment based on domain. 
	Defined into `hooks.py` as `site_app_domains`

	:return: prod|preprod|local
	:rtype: str
	"""
	from .hooks import site_app_domains as sites
	return sites[frappe.local.site] if frappe.local.site in sites else "local"


# <FRAPPE OVERRIDES

def egd_guess_language(lang_list=None) -> str:
	"""Set `frappe.local.lang` from url language segment: `/xx/...`"""
	if is_app_for_actual_site():
		from .hooks import translated_languages_for_website as languages
		if languages:
			# If language passed in url like: `url?_lang=xx`
			if frappe.local.form_dict._lang and frappe.local.form_dict._lang in languages:
				lang = frappe.local.form_dict._lang
			else:
				path = frappe.local.request.path
				# Default language first in list
				lang = languages[0]
				if len(path) >= 3 and path[1:3] in languages:
					lang = path[1:3]
			frappe.lang = frappe.local.lang = lang
			return lang
	return frappe_guess_language(lang_list)

from frappe.translate import guess_language as frappe_guess_language
frappe.translate.guess_language = egd_guess_language


def egd_resolve_redirect(path):
	if is_app_for_actual_site():
		requested = frappe.local.request.path
		restricted_to = []

		# Show access password for any host not related to production or local (staging., prod., ...)
		if site_env() == "preprod":
			user_agent = frappe.local.request.headers.get("User-Agent")
			# Allow access to site checker Pulno/0.7 (http://www.pulno.com/bot.html)
			if not user_agent or not "pulno.com/bot.html" in user_agent:
				restricted_to = ["/access"]

		if (restricted_to and requested not in restricted_to
			and not requested.startswith("/api/") and not requested.endswith((".js", ".css"))):
			if (not "preview_access" in frappe.local.request.cookies 
				or frappe.local.request.cookies["preview_access"] != frappe.local.conf.RESTRICTED_COOKIE_VALUE):
				frappe.local.flags.redirect_location = "/access"
				raise frappe.Redirect
		frappe_resolve_redirect(path)
	else:
		frappe_resolve_redirect(path)

from frappe.website.redirect import resolve_redirect as frappe_resolve_redirect
frappe.website.redirect.resolve_redirect = egd_resolve_redirect
# First import full module `render` to avoid issue when file loading from `bench`
import frappe.website.render
frappe.website.render.resolve_redirect = egd_resolve_redirect

# FRAPPE OVERRIDES>
