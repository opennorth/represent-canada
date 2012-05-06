jQuery(function ($) {
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

  $('#apibrowser pre').html(formatJSON($('#apibrowser pre').text()));

/*
  var $modal = $('#modal');

  function processModal(url) {
    $modal.find('h3').text(url);
    $.ajax({
      url: url + (url.indexOf('?') === -1 ? '?' : '&') + 'pretty=1',
      dataType: 'text',
      success: function (data) {
        var json = formatJSON(data.replace(/[?&]pretty=1/g, ''));
        $modal.find('pre').html(json.replace(/[?&]format=apibrowser/g, ''));
        $('a[href^="/"]').click(function (e) {
          processModal($(this).attr('href'));
          e.preventDefault();
        });
        $modal.modal('show');
      }
    });
  }

  $('#api button').click(function () {
    processModal($(this).parent().contents().last().text());
  });

  $modal.modal({show: false});
*/
});
