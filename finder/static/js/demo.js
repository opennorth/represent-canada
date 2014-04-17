var BASE_URL = 'https://represent.opennorth.ca',
    geocoder = new google.maps.Geocoder(),
    map,
    marker,
    featureGroup,
    representativeTemplate = _.template( // @todo Replace this one underscore dependency.
      '<div class="col-xs-6 col-sm-3 col-lg-2 representative">' +
        '<div class="avatar"><img src="<% if (photo_url) { %><%= photo_url %><% } else { %>img/silhouette.png<% } %>" alt=""></div> ' +
        '<p><% if (party_name) { %><%= party_name %><% } %> ' + '<%= elected_office %> ' +
        '<strong><% if (url) { %><a href="<%= url %>"><%= name %></a><% } else { %><%= name %><% } %></strong></p> ' +
        '<p class="district-name"><%= district_name %> <button type="button" class="btn btn-default btn-xs shape" data-url="<%= related.boundary_url %>">Map</button></p> ' +
        '<p><% if (email) { %><a href="mailto:<%= email %>">Email <%= first_name %></a><% } %></p> ' +
      '</div>'
    );

/**
 * @see http://learn.jquery.com/code-organization/deferreds/examples/
 */
function createCache(requestFunction) {
  var cache = {};
  return function (arg, callback) {
    var key = arg.toString();
    if (!cache[key]) {
      cache[key] = $.Deferred(function (defer) {
        requestFunction(defer, arg);
      }).promise();
    }
    return cache[key].done(callback);
  };
}

/**
 * @param L.LatLng latlng
 */
var getRepresentativesByLatLng = createCache(function (defer, latlng) {
  $.ajax({
    dataType: 'json',
    url: BASE_URL + '/representatives/?limit=0&point=' + latlng.lat + ',' + latlng.lng,
    success: defer.resolve,
    error: defer.reject
  });
});

/**
 * @param L.LatLng latlng
 */
var getBoundariesByLatLng = createCache(function (defer, latlng) {
  $.ajax({
    dataType: 'json',
    url: BASE_URL + '/boundaries/?contains=' + latlng.lat + ',' + latlng.lng,
    success: defer.resolve,
    error: defer.reject
  });
});

/**
 * @param string path the boundary's path
 */
var getBoundaryRepresentatives = createCache(function (defer, path) {
  $.ajax({
    dataType: 'json',
    url: BASE_URL + path + 'representatives/?limit=0',
    success: defer.resolve,
    error: defer.reject
  });
})

/**
 * @param string path the boundary's path
 */
var getBoundaryShape = createCache(function (defer, path) {
  $.ajax({
    dataType: 'json',
    url: BASE_URL + path + 'simple_shape',
    success: defer.resolve,
    error: defer.reject
  })
});

/**
 * @param L.LatLng latlng
 */
function processLatLng(latlng) {
  featureGroup.clearLayers();
  $('#map').css('visibility', 'visible');

  marker.setLatLng(latlng);
  map.panTo(latlng);

  getRepresentativesByLatLng(latlng).then(function (response) {
    var $representatives = $('<div id="representatives"></div>');
    var $row;
    $.each(response.objects, function (i, object) {
      if (i % 6 == 0) {
        $row = $('<div class="row"></div>');
        $representatives.append($row);
      }
      var $representative = $(representativeTemplate(object));
      $row.append($representative);
    });

    $('#representatives').replaceWith($representatives);

    $('#representatives').imagesLoaded().progress(function (instance, image) {
      if (!image.isLoaded) {
        $(image.img).attr('src', 'img/silhouette.png');
      }
    });
  });
}

function processAddress() {
  $('.alert').hide();
  $('#addresses').empty();

  geocoder.geocode({address: $('#address').val(), region: 'ca'}, function (results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      if (results.length > 1) {
          $('#addresses').append('<option>Select your address</option>');
        $.each(results, function (i, result) {
          $('#addresses').append('<option data-latitude="' + result.geometry.location.lat() + '" data-longitude="' + result.geometry.location.lng() + '">' + result.formatted_address + '</option>');
        });
        $('#many-results').fadeIn('slow');
      }
      else {
        processLatLng(L.latLng(results[0].geometry.location.lat(), results[0].geometry.location.lng()));
      }
    }
    else if (status == google.maps.GeocoderStatus.ZERO_RESULTS) {
      $('#no-results').fadeIn('slow');
    }
    else {
      $('#unknown-error').fadeIn('slow');
    }
  });
}

$(function ($) {
  var latlng = L.latLng(45.444369, -75.693832), // 24 Sussex Drive, Ottawa
      index = window.location.href.indexOf('#'),
      anchor;

  // Create the map, marker and feature group.
  map = L.map('map', {
    attributionControl: false,
    center: latlng,
    layers: [
      L.tileLayer('http://{s}.tiles.mapbox.com/v3/jpmckinney.hlcgg444/{z}/{x}/{y}.png')
    ],
    maxZoom: 17,
    zoom: 13,
    scrollWheelZoom: false
  });
  marker = L.marker(latlng, {draggable: true});
  featureGroup = L.featureGroup();
  map.addLayer(marker);
  map.addLayer(featureGroup);

  // Moving the marker calls the API.
  marker.on('dragend', function () {
    $('.alert').hide();
    processLatLng(marker.getLatLng());
  });

  // Geolocation calls the API.
  map.on('locationfound', function (event) {
    $('.alert').hide();
    processLatLng(event.latlng);
  });

  // Call the API if the user submits an address.
  $('#submit').click(function (event) {
    processAddress();
    event.preventDefault();
  });

  // Call the API if the user selects on an address.
  $('#addresses').change(function (event) {
    var $this = $(this).find(':selected');
    processLatLng(L.latLng($this.data('latitude'), $this.data('longitude')));
    event.preventDefault();
  });

  // Display a boundary if user clicks on a boundary name.
  $(document).on('click', '.shape', function (event) {
    featureGroup.clearLayers();
    $.scrollTo('#map', {axis: 'y', duration: 600, easing: 'easeOutQuart', offset: -40});

    getBoundaryShape($(this).data('url'), function (response) {
      featureGroup.addLayer(L.geoJson(response));
      map.fitBounds(featureGroup.getBounds());
    });

    event.preventDefault();
  });

  // Perform the first geolocation.
  if (index !== -1) { // Backwards-compatibility.
    anchor = window.location.href.substr(index + 1);
  }
  if (anchor) {
    $('#address').val(unescape(anchor));
    processAddress();
  }
  else {
    map.locate({setView: true, maxZoom: 13});
  }
});
