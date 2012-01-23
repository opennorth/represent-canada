var boundaryCache = [], shapeCache = [];
var map, marker, shape, boundary; // the displayed boundary

/**
 * Calls the API and displays the results.
 * @param L.LatLng latlng
 */
function process(latlng) {
  removeBoundary();

  // Center the marker and map on the point.
  marker.setLatLng(latlng);
  map.panTo(latlng);

  // @todo update to new API
  $.getJSON('http://boundaries.opennorth.ca/boundaries/?contains=' + latlng.lat + ',' + latlng.lng + '&callback=?', function (response) {
    console.log(response);
    // Display the list of boundaries.
    var html = '';
    $.each(response.objects, function (i, object) {
      boundaryCache[object.url] = object;
      html += '<tr><td>' + object.boundary_set_name + '</td><td><a href="#" data-url="' + object.url + '">' + object.name + '</a></td></tr>';
    });
    $('#boundaries').html(html);

    // Try to display a boundary from the same set.
    if (boundary) {
      boundary = _.find(response.objects, function (object) {
        return object.boundary_set_name == boundary.boundary_set_name;
      });
    }
    if (boundary) {
      display(boundary.url, false);
    }
  });
}

/**
 * Displays a boundary.
 * @param string url the unique url of the boundary to display
 * @param boolean fitBounds whether to set a map view that contains the boundary
 *   with the maximum zoom level possible
 */
function display(url, fitBounds) {
  removeBoundary();

  // @todo Cache these queries
  $.getJSON('http://boundaries.opennorth.ca' + url + 'simple_shape?callback=?', function (response) {
    var latlngs = [];
    var paths = [];
    $.each(response.coordinates, function (j, lines) {
      $.each(lines, function (k, points) {
        var path = [];
        $.each(points, function (m, point) {
          var latlng = new L.LatLng(point[1], point[0]);
          latlngs.push(latlng);
          path.push(latlng);
        });
        paths.push(path);
      });
    });

    $('a[data-url="' + url + '"]').addClass('selected');
    shape = new L.Polygon(paths);
    map.addLayer(shape);

    if (fitBounds) {
      map.fitBounds(new L.LatLngBounds(latlngs));
    }

    boundary = boundaryCache[url];
  });
}

/**
 * Removes any displayed boundary.
 * @note Doesn't reset +boundary+
 */
function removeBoundary() {
  if (shape) {
    map.removeLayer(shape);
    shape = undefined;
    $('#boundaries .selected').removeClass('selected');
  }
}

jQuery(function ($) {
  var geocoder = new google.maps.Geocoder();
  var latlng = new L.LatLng(45.444369, -75.693832); // 24 Sussex Drive, Ottawa

  // Create the marker. Moving the marker calls the API.
  marker = new L.Marker(latlng, {draggable: true});
  marker.on('dragend', function () {
    process(marker.getLatLng());
  });

  // Create the map. Geolocation calls the API.
  map = new L.Map('map_canvas', {
    center: latlng,
    zoom: 13,
    layers: [
      new L.TileLayer('http://{s}.tile.cloudmade.com/266d579a42a943a78166a0a732729463/51080/256/{z}/{x}/{y}.png', {
        attribution: '© 2011 <a href="http://cloudmade.com/">CloudMade</a> – Map data <a href="http://creativecommons.org/licenses/by-sa/2.0/">CCBYSA</a> 2011 <a href="http://openstreetmap.org/">OpenStreetMap.org</a> contributors – <a href="http://cloudmade.com/about/api-terms-and-conditions">Terms of Use</a>'
      })
    ],
    maxZoom: 17
  });
  map.addLayer(marker);
  map.locateAndSetView(13);
  map.on('locationfound', function (event) {
    process(event.latlng);
  });

  // http://stackoverflow.com/questions/2996431/javascript-detect-when-a-window-is-resized
  $(window).resize(function () {
    if (this.resizeTo) {
      clearTimeout(this.resizeTo);
    };
    this.resizeTo = setTimeout(function () {
      $(this).trigger('resizeend');
    }, 500);
  });
  // Keep the marker visible on resize.
  $(window).bind('resizeend', function () {
    map.panTo(marker.getLatLng());
  });

  // Geocode an address and call the API.
  $('#location-form').submit(function (event) {
    geocoder.geocode({address: $('#address').val()}, function (results, status) {
      $('#addresses').empty();
      if (status == google.maps.GeocoderStatus.OK) {
        // Display the list of addresses.
        $.each(results, function (i, result) {
          var location = result.geometry.location;
          $('#addresses').append('<a href="#" data-latitude="' + location.lat() + '" data-longitude="' + location.lng() + '">' + result.formatted_address + '</a>');
        });

        var location = results[0].geometry.location;
        process(new L.LatLng(location.lat(), location.lng()));
      }
    });
    event.preventDefault();
  });

  // Call the API if the user clicks on an address.
  $('#addresses a').live('click', function (event) {
    var $this = $(this);
    process(new L.LatLng($this.attr('data-latitude'), $this.attr('data-longitude')));
    event.preventDefault();
  });

  // Display a boundary if user clicks on a boundary name.
  $('#boundaries a').live('click', function (event) {
    var $this = $(this);
    display($this.attr('data-url'), true);
    event.preventDefault();
  });
});

/**
 * In API docs, loads and displays JSON for <pre class="loadjson" data-url="/resource/">
 * Depends on the formatJSON global function, provided by boundaryservice/jsonformatter.js
 */
function loadJSONExamples() {
  $('pre.loadjson').each(function() {
    var $el = $(this);
    if (!$el.html().length) {
      var url = $el.data('url');
      $el.append($(document.createElement('div')).addClass('url').html(url));
      if (url.indexOf('?') === -1) {
        url += '?';
      }
      else {
        url += '&';
      }
      url += 'pretty=1';
      $.ajax({
        url: url,
        dataType: 'text',
        success: function(data) {
          $el.append(formatJSON(data.replace(/[?&]pretty=1/g, '')));
        }
      });
    }
  });
}