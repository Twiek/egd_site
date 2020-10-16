
frappe.ready(function() {

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

	// one page navigation 
	$('.navbar-nav').onePageNav({
		currentClass: 'active'
	})

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
			}
			form.classList.add('was-validated')
		}, false)
	})
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
