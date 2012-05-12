jQuery(function ($) {
  if ($('#api').length) {
    $('body').scrollspy({target: '.subnav', offset: 55}); // 1 more than full height of subnav

    // http://twitter.github.com/bootstrap/assets/js/application.js
    var $window = $(window),
        $subnav = $('.subnav'),
        offset = $('.subnav').length && $('.subnav').offset().top,
        fixed = false;

    function processScroll() {
      var scrollTop = $window.scrollTop()
      if (scrollTop >= offset && !fixed) {
        fixed = true;
        $subnav.addClass('subnav-fixed');
      } else if (scrollTop <= offset && fixed) {
        fixed = false;
        $subnav.removeClass('subnav-fixed');
      }
    }
    processScroll();

    $window.on('scroll', processScroll);

    $subnav.on('click', function () {
      if (!fixed) {
        setTimeout(function () {
          $window.scrollTop($window.scrollTop() - 54); // full height of subnav
        }, 10);
      }
    });

    $('.subnav').localScroll({
      axis : 'y',
      duration : 500,
      easing : 'easeInOutExpo',
      hash : true
    });
  }

  $('#apibrowser pre').html(formatJSON($('#apibrowser pre').text()));
});
