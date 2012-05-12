jQuery(function ($) {
  if ($('#api').length) {
    var $window = $(window),
        $subnav = $('.subnav'),
        offset = $('.subnav').length && $('.subnav').offset().top;

    $('body').scrollspy({target: '.subnav'});

    $subnav.localScroll({
      axis : 'y',
      duration : 500,
      easing : 'easeInOutExpo',
      hash : true
    });

    function processScroll() {
      $subnav.toggleClass('subnav-fixed', $window.scrollTop() >= offset);
    }
    processScroll();

    $window.on('scroll', processScroll);
  }

  $('#apibrowser pre').html(formatJSON($('#apibrowser pre').text()));
});
