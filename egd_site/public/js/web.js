
import isoCountriesLanguages from '@hotosm/iso-countries-languages'
window.isoCountriesLanguages = isoCountriesLanguages

frappe.ready(function() {

	// COUNTRIES TRANSLATED
	window.context.countries = window.isoCountriesLanguages.getCountries(window.context.lang)
	$('select.select-countries').each((idx, el) => {
		$.each(window.context.countries, function(iso, label) {
			$(el).append($('<option></option>').val(iso).html(label) )
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
		const $email = $newsletter.find('[name="email"]')
		const $message_ok = $newsletter.find('.alert-success')
		$form.on('submit', function(e) {
			e.preventDefault()
			e.stopPropagation()
			subscribe()
		})
		function subscribe() {
			const email = $email.val()
			if (email && validate_email(email)) {
				$email.attr('disabled', true)
				$submit.html(__('Subscribing...')).attr('disabled', true)
				return frappe.call({
					type: 'POST',
					method: 'egd_site.tools.subscribe',
					args: { 'email': email, '_lang': window.context.lang },
					callback: r => {
						if (!r.exc) {
							$message_ok.show()
							$form.hide()
						} else {
							$submit.html(__('Error with subscription')).addClass('btn-danger').attr('disabled', false)
							$email.val('').attr('disabled', false)
						}
					},
				})
			}
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
