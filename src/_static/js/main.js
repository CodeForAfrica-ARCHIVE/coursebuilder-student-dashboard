  function showPage(pageName) {
    $('#' + pageName).show();
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

