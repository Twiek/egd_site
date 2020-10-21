from __future__ import unicode_literals
import frappe


no_cache = 1
sitemap = 0


def get_context(context):

	import os
	import io
	# from frappe.translate import get_messages_for_app
	from frappe.translate import deduplicate_messages
	from frappe.translate import get_all_messages_from_js_files
	from frappe.translate import get_server_messages
	from frappe.translate import get_translation_dict_from_file
	from csv import writer

	app = "egd_site"
	messages = []
	# # full app messages
	# messages.extend(get_messages_for_app(app))
	# app_include_files
	messages.extend(get_all_messages_from_js_files(app))
	# server_messages
	messages.extend(get_server_messages(app))
	messages = deduplicate_messages(messages)

	ctx_lang = frappe._dict({
		"translated": frappe._dict(),
		"segments_as_txt": frappe._dict(),
	})

	languages = frappe.get_hooks("translated_languages_for_website")
	for lang in languages:
		path = os.path.join(frappe.get_pymodule_path(app), "translations", lang + ".csv")
		data = get_translation_dict_from_file(path, lang, app)
		print(data)
		ctx_lang["translated"][lang] = data

		mem_file = io.StringIO()
		w = writer(mem_file, lineterminator="\n")
		for p, m in messages:
			translated = ctx_lang["translated"][lang][m] if m in ctx_lang["translated"][lang] else m
			w.writerow([p if p else '', m, translated])

		ctx_lang["segments_as_txt"][lang] = mem_file.getvalue()

	context["languages_data"] = ctx_lang
