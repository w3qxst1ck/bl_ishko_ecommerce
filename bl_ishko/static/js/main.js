/*-----------------------------------------------------------------------------------*/
/* 		SEBIAN MAIN JS FILE
/*-----------------------------------------------------------------------------------*/
$(document).ready(function($) {
"use strict"
/*-----------------------------------------------------------------------------------*/
/* 	LOADER
/*-----------------------------------------------------------------------------------*/
$(window).load(function() {
	$("#loader").delay(500).fadeOut("slow");
});
/*-----------------------------------------------------------------------------------*/
/*		STICKY NAVIGATION
/*-----------------------------------------------------------------------------------*/
$(".sticky").sticky({topSpacing:0});
/*-----------------------------------------------------------------------------------*/
/* 	ANIMATION
/*-----------------------------------------------------------------------------------*/
var wow = new WOW({
    boxClass:     'animate',      // animated element css class (default is wow)
    animateClass: 'animated', // animation css class (default is animated)
    offset:       100,          // distance to the element when triggering the animation (default is 0)
    mobile:       false        // trigger animations on mobile devices (true is default)
});
wow.init();
/*-----------------------------------------------------------------------------------*/
/* 	PRODUCTS SLIDER
/*-----------------------------------------------------------------------------------*/
$(".product-slides").owlCarousel({ 
    items : 1,
	autoplay:false,
	autoplayHoverPause:true,
	singleItem	: true,
	navText: ["<i class='fa fa-angle-left'></i>","<i class='fa fa-angle-right'></i>"],
	lazyLoad:true,
	nav: true,
	animateOut: 'fadeOut'	
});
/*-----------------------------------------------------------------------------------*/
/* 	ABOUT CLIENT SLIDER
/*-----------------------------------------------------------------------------------*/
$(".clients-about-slider").owlCarousel({ 
	autoplay:false,
	autoplayHoverPause:true,
	singleItem	: true,
	navText: ["<i class='fa fa-angle-left'></i>","<i class='fa fa-angle-right'></i>"],
	lazyLoad:true,
	nav: true,
	margin:30,
	responsive:{
        0:{
            items:1
        },
        600:{
            items:2
        },
        1200:{
            items:3,
			nav: false
        }}
});
/*-----------------------------------------------------------------------------------*/
/* 	PRODUCTS SLIDER
/*-----------------------------------------------------------------------------------*/
$(".testi-slides").owlCarousel({ 
    items : 1,
	autoplay:true,
	loop:true,
	autoplayHoverPause:true,
	singleItem	: true,
	navText: ["<i class='fa fa-angle-left'></i>","<i class='fa fa-angle-right'></i>"],
	lazyLoad:true,
	nav: true,
	animateOut: 'fadeOut'	
});
/*-----------------------------------------------------------------------------------*/
/* 	ADD TO CART
/*-----------------------------------------------------------------------------------*/
$("#product-color").on('change', function () {
	let color_value = this.value;
	let color_input = $("#color_input");
	color_input.val(color_value);
});

$("select#product-size").on('change', function () {
	let size_value = this.value;
	let size_input = $(this).siblings('input');
	size_input.val(size_value);
	let hiddenP = $('#ajax-add-to-cart-p');
	hiddenP.attr('hidden', 'true');
});

$("#product-quantity").on('change', function () {
	let quantity_value = this.value;
	let quantity_input = $("#quantity_input");
	quantity_input.val(quantity_value);
	let hiddenP = $('#ajax-add-to-cart-p');
	hiddenP.attr('hidden', 'true');

	// check 0
	if (quantity_value == '0') {
		$("#ajax-add-to-cart").prop("disabled", true);
	} else {
		$("#ajax-add-to-cart").prop("disabled", false);
	};
});

/*-----------------------------------------------------------------------------------*/
/* 	SEARCH NAVBAR
/*-----------------------------------------------------------------------------------*/
$("#select-search").on('change', function () {
	let searched_category = this.value;
	let hidden_input_category = $("#category-input");
	hidden_input_category.val(searched_category);
});
/*-----------------------------------------------------------------------------------*/
/* 	PAYMENT METHODS
/*-----------------------------------------------------------------------------------*/
$("#checkbox-cash").on('change', function () {
	$("#checkbox-card").removeAttr("checked");
});
$("#checkbox-card").on('change', function () {
	$("#checkbox-cash").removeAttr("checked");
});
/*-----------------------------------------------------------------------------------*/
/* 	COPY URL
/*-----------------------------------------------------------------------------------*/
$("a#share-product").on('click', function () {
	var dummy = document.createElement('input'),
	text = window.location.href;
	document.body.appendChild(dummy);
	dummy.value = text;
	dummy.select();
	document.execCommand('copy');
	document.body.removeChild(dummy);
});
$("a#share-product1").on('click', function () {
	var dummy = document.createElement('input');
	var my_domen = "http://127.0.0.1:8000";
	var product_url = $(this).parents().siblings('input').val();
	var text = my_domen + product_url;
	document.body.appendChild(dummy);
	dummy.value = text;
	dummy.select();
	document.execCommand('copy');
	document.body.removeChild(dummy);
});

/*-----------------------------------------------------------------------------------*/
/* 	PRICE SLIDER
/*-----------------------------------------------------------------------------------*/
$("#price-min").on('DOMSubtreeModified', function () {
	var minPriceValue = $(this).text().replace('₽', '');
	var minPriceInput = $("#price-min-input");
	minPriceInput.val(minPriceValue);
});
$("#price-max").on('DOMSubtreeModified', function () {
	var maxPriceValue = $(this).text().replace('₽', '');
	var maxPriceInput = $("#price-max-input");
	maxPriceInput.val(maxPriceValue);
});

/*-----------------------------------------------------------------------------------*/
/* 	ABOUT CLIENT SLIDER
/*-----------------------------------------------------------------------------------*/
$(".new-col-slide").owlCarousel({ 
	autoplay:false,
	autoplayHoverPause:true,
	singleItem	: true,
	navText: ["<i class='fa fa-angle-left'></i>","<i class='fa fa-angle-right'></i>"],
	lazyLoad:true,
	nav: false,
	margin:30,
	responsive:{
        0:{
            items:1
        },
        600:{
            items:2
        },
        1200:{
            items:3,
        }}
});
/*-----------------------------------------------------------------------------------*/
/* 		FEATURE SLIDER
/*-----------------------------------------------------------------------------------*/
$(".fur-slide").owlCarousel({ 
	autoplay:true,
	autoplayHoverPause:true,
	singleItem	: true,
	navText: ["<i class='fa fa-angle-left'></i>","<i class='fa fa-angle-right'></i>"],
	lazyLoad:true,
	nav: false,
	margin:0,
	responsive:{
        0:{
            items:1
        },
        1000:{
            items:2,
        }}
});
/*-----------------------------------------------------------------------------------*/
/* 		CLIENTS LOGO SLIDE
/*-----------------------------------------------------------------------------------*/
$(".client-slide").owlCarousel({ 
	autoplay:true,
	autoplayHoverPause:true,
	singleItem	: true,
	navText: ["<i class='fa fa-angle-left'></i>","<i class='fa fa-angle-right'></i>"],
	lazyLoad:true,
	nav: false,
	loop:true,
	margin:30,
	animateOut: 'fadeOut',	
	responsive:{
        0:{
            items:1
        },
        600:{
            items:2
        },
        800:{
            items:3
        },
        1200:{
            items:4
        }}	
});
/*-----------------------------------------------------------------------------------*/
/* 		BANNER ITEMS SLIDER
/*-----------------------------------------------------------------------------------*/
$(".bnr-items-slider").owlCarousel({ 
	autoplay:true,
	autoplayHoverPause:true,
	singleItem	: true,
	navText: ["<i class='fa fa-angle-left'></i>","<i class='fa fa-angle-right'></i>"],
	lazyLoad:true,
	nav: false,
	loop:true,
	margin:0,
	animateOut: 'fadeOut',	
	responsive:{
        0:{
            items:1
        },
        600:{
            items:2
        },
        800:{
            items:2
        },
		1350:{
            items:3
        },
        1600:{
            items:4
        }}	
});

/*-----------------------------------------------------------------------------------*/
/*    POPUP VIDEO
/*-----------------------------------------------------------------------------------*/
$('.popup-vedio').magnificPopup({
	type: 'inline',
	fixedContentPos: false,
	fixedBgPos: true,
	overflowY: 'auto',
	closeBtnInside: true,
	preloader: true,
	midClick: true,
	removalDelay: 300,
	mainClass: 'my-mfp-slide-bottom'
});
$('.gallery-pop').magnificPopup({
	delegate: 'a',
	type: 'image',
	tLoading: 'Loading image #%curr%...',
	mainClass: 'mfp-img-mobile',
	gallery: {
		enabled: true,
		navigateByImgClick: true,
		preload: [0,1] // Will preload 0 - before current, and 1 after the current image
	},
	image: {
		tError: '<a href="%url%">The image #%curr%</a> could not be loaded.',
		titleSrc: function(item) {
			return item.el.attr('title') + '';}}
});
/*-----------------------------------------------------------------------------------*/
/* 	SLIDER REVOLUTION
/*-----------------------------------------------------------------------------------*/
jQuery('.tp-banner').show().revolution({
	dottedOverlay:"none",
	delay:10000,
	startwidth:1170,
	startheight:700,
	navigationType:"bullet",
	navigationArrows:"solo",
	navigationStyle:"preview4",
	parallax:"mouse",
	parallaxBgFreeze:"on",
	parallaxLevels:[7,4,3,2,5,4,3,2,1,0],												
	keyboardNavigation:"on",						
	shadow:0,
	fullWidth:"on",
	fullScreen:"on",
	shuffle:"off",						
	autoHeight:"off",						
	forceFullWidth:"off",	
	fullScreenOffsetContainer:""	
});

/*-----------------------------------------------------------------------------------*/
/* 	SLIDER REVOLUTION
/*-----------------------------------------------------------------------------------*/
jQuery('.tp-banner-fix').show().revolution({
	dottedOverlay:"none",
	delay:10000,
	startwidth:1170,
	startheight:700,
	navigationType:"bullet",
	navigationArrows:"solo",
	navigationStyle:"preview4",
	parallax:"mouse",
	parallaxBgFreeze:"on",
	parallaxLevels:[7,4,3,2,5,4,3,2,1,0],												
	keyboardNavigation:"on",						
	fullWidth:"off",
	fullScreen:"off"
});
/*-----------------------------------------------------------------------------------*/
/* 	SLIDER REVOLUTION
/*-----------------------------------------------------------------------------------*/
jQuery('.tp-banner-box').show().revolution({
	dottedOverlay:"none",
	delay:10000,
	startwidth:1170,
	startheight:780,
	navigationType:"bullet",
	navigationArrows:"solo",
	navigationStyle:"preview4",
	parallax:"mouse",
	parallaxBgFreeze:"on",
	parallaxLevels:[7,4,3,2,5,4,3,2,1,0],												
	keyboardNavigation:"on",						
	fullWidth:"on",
	fullScreen:"off"
});
/*-----------------------------------------------------------------------------------*/
/* 		Parallax
/*-----------------------------------------------------------------------------------*/
$('.images-slider').flexslider({
  animation: "fade",
  controlNav: "thumbnails"
});
/*-----------------------------------------------------------------------------------*/
/*	Go TO TOP
/*-----------------------------------------------------------------------------------*/
var offset = 300,
	//browser window scroll (in pixels) after which the "back to top" link opacity is reduced
	offset_opacity = 1200,
	//duration of the top scrolling animation (in ms)
	scroll_top_duration = 700,
	//grab the "back to top" link
	$back_to_top = $('.cd-top');

//hide or show the "back to top" link
$(window).scroll(function(){
	( $(this).scrollTop() > offset ) ? $back_to_top.addClass('cd-is-visible') : $back_to_top.removeClass('cd-is-visible cd-fade-out');
	if( $(this).scrollTop() > offset_opacity ) { 
		$back_to_top.addClass('cd-fade-out');
	}
});
//smooth scroll to top
$back_to_top.on('click', function(event){
	event.preventDefault();
	$('body,html').animate({
		scrollTop: 0 ,
	 	}, scroll_top_duration
);
});
});


