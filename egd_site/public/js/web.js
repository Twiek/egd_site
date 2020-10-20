
import isoCountriesLanguages from '@hotosm/iso-countries-languages'
// window.isoCountriesLanguages = isoCountriesLanguages

frappe.ready(function() {

	// COUNTRIES TRANSLATED
	// If not available for actual user language return countries in English
	let countries = isoCountriesLanguages.getCountries(
		isoCountriesLanguages.getSupportedLangs().indexOf(window.context.lang) > -1 ? window.context.lang : 'en'
	)
	let countries_sorted = Object.keys(countries).sort((a, b) => countries[a].localeCompare(countries[b]))
	$('select.select-countries').each((idx, el) => {
		$.each(countries_sorted, (idx, iso) => {
			$(el).append($('<option></option>').val(iso).html(countries[iso]))
		})
	})


	$('#preloader').fadeOut()


	// // Sticky Nav
	// $(window).on('scroll', function() {
	// 	if ($(window).scrollTop() > 200) {
	// 		$('.scrolling-navbar').addClass('top-nav-collapse')
	// 	} else {
	// 		$('.scrolling-navbar').removeClass('top-nav-collapse')
	// 	}
	// })


	/*====================================
	slick menu js
	======================================*/
	let logo_path=$('.mobile-menu').data('logo')
	$('#navbarCollapse').slicknav({
		appendTo:'.mobile-menu',
		removeClasses:false,
		label:'',
		closedSymbol:'<i class="lni-chevron-right"><i/>',
		openedSymbol:'<i class="lni-chevron-down"><i/>',
		brand:'<a href="index.html"><img src="'+logo_path+'" class="img-responsive" alt="logo"></a>'
	})


	/* WOW Scroll Spy
	========================================================*/
	let wow = new WOW({
		//disabled for mobile
		mobile: false
	})
	wow.init()


	/* Back Top Link active
	========================================================*/
	let offset = 200
	$(window).scroll(function() {
		if ($(this).scrollTop() > offset) {
			$('.back-to-top').fadeIn(400)
		} else {
			$('.back-to-top').fadeOut(400)
		}
	})

	$('.back-to-top').on('click',function(event) {
		event.preventDefault()
		$('html, body').animate({
			scrollTop: 0
		}, 600)
		return false
	})


	// BS FORM VALIDATIONS
	const FORMS = document.getElementsByClassName('bs-validation')
	// Loop over them and prevent submission
	Array.prototype.filter.call(FORMS, function(form) {
		form.addEventListener('submit', function(event) {
			if (form.checkValidity() === false) {
				event.preventDefault()
				event.stopPropagation()
				$(form).addClass('shake animated').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
					$(this).removeClass('shake animated')
				})
			}
			form.classList.add('was-validated')
		}, false)
	})


	// SUBSCRIBE
	const $newsletter = $('.form-subscribe')
	if ($newsletter.length) {
		const $form = $newsletter.find('form')
		const $submit = $newsletter.find('button')
		const $message_ok = $newsletter.find('.alert-success')
		const $f_email = $newsletter.find('[name="email"]')
		$form.on('submit', function(e) {
			e.preventDefault()
			e.stopPropagation()
			if (e.target.checkValidity() && validate_email($f_email.val())) {
				send()
			}
		})
		function send() {
			$f_email.attr('disabled', true)
			$submit.html(__('Subscribing...')).attr('disabled', true)
			return frappe.call({
				type: 'POST',
				method: 'egd_site.tools.subscribe',
				args: { 'email': $f_email.val(), '_lang': window.context.lang },
				callback: r => {
					if (!r.exc) {
						$message_ok.show()
						$form.hide()
					} else {
						$submit.html(__('Error with form')).addClass('btn-danger').attr('disabled', false)
						$f_email.val('').attr('disabled', false)
					}
				},
			})
		}
	}


	// CONTACT
	const $contact = $('.form-contact')
	if ($contact.length) {
		const $form = $contact.find('form')
		const $submit = $contact.find('button')
		const $message_ok = $contact.find('.alert-success')
		const $f_email = $contact.find('[name="email"]')
		const $f_fullname = $contact.find('[name="fullname"]')
		const $f_country = $contact.find('[name="country"]')
		const $f_subject = $contact.find('[name="subject"]')
		const $f_message = $contact.find('[name="message"]')
		const $f_accepted = $contact.find('[name="accepted"]')
		$form.on('submit', function(e) {
			e.preventDefault()
			e.stopPropagation()
			if (e.target.checkValidity() && validate_email($f_email.val())) {
				send()
			}
		})
		function send() {
			$f_email.attr('disabled', true)
			$submit.html(__('Sending...')).attr('disabled', true)
			let opts = {
				type: 'POST',
				method: 'egd_site.tools.contact',
				args: {
					email: $f_email.val(),
					full_name: $f_fullname.val(),
					country_code: $f_country.val(),
					subject: $f_subject.val(),
					message: $f_message.val(),
					language: window.context.lang,
				},
				callback: r => {
					if (!r.exe && r.message == 'success') {
						$message_ok.show()
						$form.hide()
					} else {
							$submit.html(__('Error with form')).addClass('btn-danger').attr('disabled', false)
							$f_email.val('').attr('disabled', false)
					}
				},
			}
			frappe.call(opts)
		}
	}

})



// <FRAPPE OVERRIDES
// <Override call from /frappe/public/js/frappe/request.js
frappe.call_cloned = frappe.call.bind({})
frappe.call = function(opts) {
	if (opts['method'] == 'frappe.website.doctype.website_settings.website_settings.is_chat_enabled') {
		return false
	}
	return frappe.call_cloned(opts)
}
// Override call from /frappe/public/js/frappe/request.js>
// FRAPPE OVERRIDES>
