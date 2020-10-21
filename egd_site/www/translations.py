from __future__ import unicode_literals
import frappe


no_cache = 1
sitemap = 0


def get_context(context):

	import io
	# from frappe.translate import get_messages_for_app
	from frappe.translate import deduplicate_messages
	from frappe.translate import get_all_messages_from_js_files
	from frappe.translate import get_server_messages
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
	# messages.sort(key = lambda x: x[0])

	mem_file = io.StringIO()
	w = writer(mem_file, lineterminator="\n")
	for p, m in messages:
		w.writerow([p if p else '', m, m])

	print(mem_file.getvalue())

	context["translations"] = mem_file.getvalue()
