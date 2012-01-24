jQuery(function ($) {
  // Loads and displays JSON for <pre class="loadjson" data-url="/resource/">.
  $('pre.loadjson').each(function () {
    var $this = $(this);
    if ($this.is(':empty')) {
      var url = $this.data('url');
      $this.append('<div class="url">' + url + '</div>');
      $.ajax({
        url: url + (url.indexOf('?') === -1 ? '?' : '&') + 'pretty=1',
        dataType: 'text',
        success: function (data) {
          $this.append(formatJSON(data.replace(/[?&]pretty=1/g, '')));
        }
      });
    }
  });
});