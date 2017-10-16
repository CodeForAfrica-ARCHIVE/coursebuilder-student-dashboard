window.addEventListener('WebComponentsReady', function documentReady() {
  $('.button-collapse').sideNav();
  $('.dropdown-button').dropdown();
  $('ul.tabs').tabs();
  $('.collapsible').collapsible();

  $('.slider-carousel').owlCarousel({
    loop: true,
    margin: 10,
    autoplay: true,
    autoplayTimeout: 3000,
    autoplayHoverPause: false,
    dots: false,
    items: 1
  });
  
  $('.awards-carousel').owlCarousel({
    loop: true,
    margin: 10,
    autoplay: true,
    autoplayTimeout: 1000,
    autoplayHoverPause: false,
    dots: false,
    items: 4
  });

  $('.how-carousel').owlCarousel({
    loop: true,
    margin: 10,
    nav: true,
    navText: ['<i class="ion-ios-arrow-left"></i>', '<i class="ion-ios-arrow-right"></i>'],
    items: 1
  });

  function showPage(pageName) {
    $('.page-wrapper').hide();
    $('#' + pageName).show();
    $('.nav-link').removeClass('active-link');
    $('.home-main-menu a[href="#!' + pageName + '"]').addClass('active-link');
  }

  var pageLinks = [
    'student-dashboard'
  ];

  pageLinks.forEach(function (name) {
    $('body').on('click', 'a[href="' + window.location.origin + '/#!' + name + '"]', function () {
      showPage(name);
    });

    if (window.location.href.substr(-name.length) === name) {
      showPage(name);
    }
  });

  var dashboardAccordionInitialized = false;
  $('body').on('click', '#student-dashboard .collapsible', function () {
    if (!dashboardAccordionInitialized) {
      $(this).collapsible('open', 0);
      dashboardAccordionInitialized = true;
      $('.collapsible').collapsible();
    }
  });
});
