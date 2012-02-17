var geocoder = new google.maps.Geocoder();
var latlngCache = [], boundaryCache = [], shapeCache = [], repCache = {};
var map, marker, shape, boundary; // the displayed boundary

/**
 * Calls the API and displays the boundaries that contain the given point.
 * @param L.LatLng latlng
 */
function processLatLng(latlng) {
  var key = latlng.toString();

  removeBoundary();

  // Center the marker and map on the point.
  marker.setLatLng(latlng);
  map.panTo(latlng);

  // Call the API.
  if (key in latlngCache) {
    processLatLngCallback(latlng);
  }
  else {
    $.getJSON('/boundaries/?contains=' + latlng.lat + ',' + latlng.lng, function (response) {
      latlngCache[key] = response;
      processLatLngCallback(latlng);
    });
  }
}

var boundaryListRowTemplate = _.template('<tr><td><%= boundary_set_name %></td>' +
    '<td class="boundary-name"><a href="#" class="display-shape" data-url="<%= url %>"><%= name %></a>' +
    ' &nbsp;<span class="label"><a href="<%= url %>?format=apibrowser">API</a></span></td></tr>');

/**
 * Displays the boundaries that contain the given point.
 * @param L.LatLng latlng
 * @note expects the API to have already been called
 * @private
 */
function processLatLngCallback(latlng) {
  var key = latlng.toString();

  // Display the boundaries.
  $('#boundaries tr').remove();
  $.each(latlngCache[key].objects, function (i, object) {
    boundaryCache[object.url] = object;
    var $row = $(boundaryListRowTemplate(object));
    $('#boundaries').append($row);

    // And add representative info
    if (repCache[object.url]) {
      displayRep(object.url, repCache[object.url], $row);
    }
    else {
      $.getJSON(object.url + 'representatives/', function(data) {
        repCache[object.url] = data;
        displayRep(object.url, data, $row);
      });
    }
  });

  // Try to display a boundary from the same set.
  if (boundary) {
    boundary = _.find(latlngCache[key].objects, function (object) {
      return object.boundary_set_name == boundary.boundary_set_name;
    });
  }
  if (boundary) {
    displayBoundary(boundary.url, false);
  }
}

/**
 * Appends the names of representatives to a boundary name.
 * @param boundaryURL the URL of the corresponding boundary
 * @param data Parsed JSON from a districts/representatives/ call
 * @param $row jQuery object for the <tr> containing the boundary name
 */
function displayRep(boundaryURL, data, $row) {
  _.each(data.objects, function(rep) {
    $row.find('td.boundary-name').append('<br>' + rep.elected_office + ': ' +
        '<a href="' + boundaryURL + 'representatives/?' +
        $.param({ elected_office: rep.elected_office, format: 'apibrowser'}) + '">' +
        rep.name + '</a>');
  });
}

/**
 * Calls the API and displays a boundary polygon.
 * @param string url the unique url of the boundary to display
 * @param boolean fitBounds whether to set a map view that contains the boundary
 *   with the maximum zoom level possible
 */
function displayBoundary(url, fitBounds) {
  removeBoundary();

  // Call the API.
  if (url in shapeCache) {
    displayBoundaryCallback(url, fitBounds);
  }
  else {
    $.getJSON(url + 'simple_shape', function (response) {
      shapeCache[url] = response;
      displayBoundaryCallback(url, fitBounds);
    });
  }
}

/**
 * Displays a boundary polygon.
 * @param string url the unique url of the boundary to display
 * @param boolean fitBounds whether to set a map view that contains the boundary
 *   with the maximum zoom level possible
 * @note expects the API to have already been called
 * @private
 */
function displayBoundaryCallback(url, fitBounds) {
  // Parse the API response.
  var latlngs = [];
  var paths = [];
  $.each(shapeCache[url].coordinates, function (j, lines) {
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

  // Opposite of removeBoundary()
  $('a[data-url="' + url + '"]').parents('tr').addClass('selected');
  shape = new L.Polygon(paths);
  map.addLayer(shape);

  // Only fit bounds if clicking on boundary name.
  if (fitBounds) {
    map.fitBounds(new L.LatLngBounds(latlngs));
  }

  boundary = boundaryCache[url];
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

function processAddress() {
  $('#addresses').hide().empty();
  geocoder.geocode({address: $('#address').val()}, function (results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      if (results.length > 1) {
        // Display the list of addresses.
        $.each(results, function (i, result) {
          var location = result.geometry.location;
          $('#addresses').append('<option data-latitude="' + location.lat() + '" data-longitude="' + location.lng() + '">' + result.formatted_address + '</option>');
        });
        $('#addresses').show();
      }

      var location = results[0].geometry.location;
      processLatLng(new L.LatLng(location.lat(), location.lng()));
    }
  });
}

jQuery(function ($) {
  var latlng = new L.LatLng(45.444369, -75.693832); // 24 Sussex Drive, Ottawa

  // Create the marker.
  marker = new L.Marker(latlng, {draggable: true});

  // Moving the marker calls the API.
  marker.on('dragend', function () {
    $('#addresses').hide();
    processLatLng(marker.getLatLng());
  });

  // Create the map.
  map = new L.Map('map', {
    center: latlng,
    zoom: 13,
    layers: [
      new L.TileLayer('http://{s}.tile.cloudmade.com/266d579a42a943a78166a0a732729463/51080/256/{z}/{x}/{y}.png', {
        attribution: '© 2011 <a href="http://cloudmade.com/">CloudMade</a> – Map data <a href="http://creativecommons.org/licenses/by-sa/2.0/">CCBYSA</a> 2011 <a href="http://openstreetmap.org/">OpenStreetMap.org</a> – <a href="http://cloudmade.com/about/api-terms-and-conditions">Terms of Use</a>'
      })
    ],
    maxZoom: 17
  });

  // Geolocation calls the API.
  map.on('locationfound', function (event) {
    $('#addresses').hide();
    processLatLng(event.latlng);
  });

  map.addLayer(marker);
  map.attributionControl.setPrefix('');

  // Perform the first geolocation.
  var address = store.get('address');
  if (address) {
    $('#address').val(address);
    processAddress();
  }
  else {
    map.locateAndSetView(13);
  }

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
  $('#submit').click(function (event) {
    store.set('address', $('#address').val());
    processAddress();
    event.preventDefault();
  });

  // Call the API if the user clicks on an address.
  $('#addresses').live('change', function (event) {
    var $this = $(this).find(':selected');
    processLatLng(new L.LatLng($this.data('latitude'), $this.data('longitude')));
    event.preventDefault();
  });

  // Display a boundary if user clicks on a boundary name.
  $('#boundaries a.display-shape').live('click', function (event) {
    var $this = $(this);
    displayBoundary($this.data('url'), true);
    event.preventDefault();
  });
});
