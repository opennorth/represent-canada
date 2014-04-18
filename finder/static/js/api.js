$(function () {
  var $apibrowser = $('#apibrowser');
  if ($apibrowser.length) {
    var $pre = $apibrowser.find('pre');
    $pre.html(formatJSON($pre.text()));
  }
});
