
from __future__ import unicode_literals
import frappe
from jinja2.runtime import Context


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

		# # Below lines will override ALL context variables previously generated
		# frappe.local.response.context["title"] = context.metatags["title"] + " | PEPE"
		# 	# frappe.get_hooks("AE_HTML_TITLE_SUFFIX")[0]
		# 	# if frappe.get_hooks("AE_HTML_TITLE_SUFFIX")
		# 	# else ""


		print("XXX COMPROBAR QUE LOS METATAGS SE APLICAN!!!!!")

		# # context.base_template_path = app_base[0] if app_base else "templates/base.html"
		# if not "metatags" in context:
		# 	context.metatags = frappe._dict({})

		# context.metatags["lang"] = frappe.local.lang
		# context.metatags["url"] = context.url
		# context.metatags["og:url"] = context.url

		# # If blog image or no default use the "summary_large_image" value
		# if "image" in context.metatags and context.metatags["image"]:
		# 	context.metatags["twitter:card"] = "summary_large_image"
		# else:
		# 	context.metatags["image"] = frappe.utils.get_url() + "/assets/egd_site/images/effective-giving-day.svg"
		# 	context.metatags["twitter:card"] = "summary"

		# if not "title" in context.metatags:
		# 	if "meta_title" in context:
		# 		context.metatags["title"] = context["meta_title"]
		# 	elif context.title:
		# 		context.metatags["title"] = context.title
		# 	# Add title suffix except for home
		# 	if "path" in context and context["path"] != "":
		# 		context.metatags["title"] += (
		# 			frappe.get_hooks("AE_HTML_TITLE_SUFFIX")[0]
		# 			if frappe.get_hooks("AE_HTML_TITLE_SUFFIX")
		# 			else ""
		# 		)

		# if not "description" in context.metatags:
		# 	if "meta_description" in context:
		# 		context.metatags["description"] = context["meta_description"]


	print(context)
	return context


# https://api.ip2country.info/ip?5.6.7.8
# https://apility.io/search/5.6.7.8
# https://ipgeolocation.io/pricing.html
