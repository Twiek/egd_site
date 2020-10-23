---
;title: HTML head title. Remove coment character ";" to be applied
;meta_description: META description. Remove coment character ";" to be applied
---

{% extends "templates/web.html" %}


{% block header %}
	{% block hero %}
		{% include "templates/includes/hero.html" %}
	{% endblock %}
	{% include "templates/includes/header.html" %}
{% endblock %}


{% block page_container %}


{% include "templates/includes/section-about.html" %}


{% include "templates/includes/section-why.html" %}


{% include "templates/includes/section-agenda.html" %}


{% include "templates/includes/section-speakers.html" %}


{% include "templates/includes/section-partners.html" %}


{% endblock %}


{% block script %}
{% endblock %}
