var geocoder = new google.maps.Geocoder();
var latlngCache = [],
    boundaryCache = [],
    shapeCache = [],
    representativeCache = {};
var map, marker, shape, boundary; // the displayed boundary

var boundaryTemplate = _.template('<div class="row boundary">' +
      '<div class="span6">' +
        '<h3>' +
          '<a href="#" class="shape" data-url="<%= url %>"><%= name %></a> ' +
          '<small><%= boundary_set_name %></small> ' +
          '<a class="label" href="<%= url %>?format=apibrowser">JSON</a> ' +
        '</h3>' +
      '</div>' +
    '</div>'),
   representativeTemplate = _.template('<div class="span1">' +
      '<% if (photo_url) { %><img src="<%= photo_url %>" width="60"><% } else { %>&nbsp;<% } %>' +
    '</div>' +
    '<div class="span5">' +
      '<h4>' +
        '<% if (url) { %><a href="<%= url %>"><%= name %></a><% } else { %><%= name %><% } %> ' +
        '<a class="label" href="<%= related.boundary_url %>representatives/?elected_office=<%= elected_office %>&format=apibrowser">JSON</a> ' +
      '</h4>' +
      '<p>' +
        '<% if (party_name) { %><%= party_name %><% } %> ' +
        '<%= elected_office %> at <%= representative_set_name %>' +
        '<% if (email) { %><br><a href="mailto:<%= email %>"><%= email %></a><% } %>' +
        '<% if (personal_url) { %><br><a href="<%= personal_url %>"><%= personal_url %></a><% } %>' +
      '</p> ' +
    '</div>');

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
    $.getJSON('http://represent.opennorth.ca/boundaries/?contains=' + latlng.lat + ',' + latlng.lng + '&callback=?', function (response) {
      latlngCache[key] = response;
      processLatLngCallback(latlng);
    });
  }
}

/**
 * Displays the boundaries that contain the given point.
 * @param L.LatLng latlng
 * @note expects the API to have already been called
 * @private
 */
function processLatLngCallback(latlng) {
  var key = latlng.toString();

  // Display the boundaries.
  $('#boundaries').empty();
  $.each(latlngCache[key].objects, function (i, object) {
    boundaryCache[object.url] = object;
    var $row = $(boundaryTemplate(object));
    $('#boundaries').append($row);

    // And add representative info
    if (object.url in representativeCache) {
      displayRepresentative(object.url, $row);
    }
    else {
      $.getJSON('http://represent.opennorth.ca' + object.url + 'representatives/' + '?callback=?', function (response) {
        representativeCache[object.url] = response;
        displayRepresentative(object.url, $row);
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
 * Appends information on representatives to a boundary DOM node.
 * @param string url the unique URL of the corresponding boundary
 * @param $row jQuery object of the boundary DOM node
 */
function displayRepresentative(url, $row) {
  _.each(representativeCache[url].objects, function (object) {
    $row.append($(representativeTemplate(object)));
  });
}

/**
 * Calls the API and displays a boundary polygon.
 * @param string url the unique URL of the boundary to display
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
    $.getJSON('http://represent.opennorth.ca' + url + 'simple_shape' + '?callback=?', function (response) {
      shapeCache[url] = response;
      displayBoundaryCallback(url, fitBounds);
    });
  }
}

/**
 * Displays a boundary polygon.
 * @param string url the unique URL of the boundary to display
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
  $('a[data-url="' + url + '"]').parents('.boundary').addClass('selected');
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
          $('#addresses').append('<option data-latitude="' + result.geometry.location.lat() + '" data-longitude="' + result.geometry.location.lng() + '">' + result.formatted_address + '</option>');
        });
        $('#addresses').show();
      }

      processLatLng(new L.LatLng(results[0].geometry.location.lat(), results[0].geometry.location.lng()));
    }
  });
}

jQuery(function ($) {
  if ($('#map').length) {
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
    $('.shape').live('click', function (event) {
      var $this = $(this);
      displayBoundary($this.data('url'), true);
      event.preventDefault();
    });
  }
});
