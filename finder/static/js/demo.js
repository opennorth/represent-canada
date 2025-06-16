/**
 * @see https://learn.jquery.com/code-organization/deferreds/examples/
 */
function createCache(url) {
  var cache = {};
  return function (arg) {
    var key = arg.toString();
    if (!cache[key]) {
      cache[key] = $.ajax({dataType: 'json', url: url(arg)});
    }
    return cache[key];
  };
}

/**
 * @param L.LatLng latlng
 */
var getRepresentativesByLatLng = createCache(function (latlng) {
  return '/representatives/?limit=0&point=' + latlng.lat + ',' + latlng.lng;
});

/**
 * @param string path the boundary's path
 */
var getBoundaryShape = createCache(function (path) {
  return path + 'simple_shape';
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
    var representatives = response.objects.slice(),
        groups = {},
        order = 'MP|MHA|MLA|MNA|MPP|Chair|Maire|Mayor|Regional Chair|Warden|Deputy Mayor|Deputy Warden|Councillor at Large|Regional Councillor|Conseiller|Councillor|Commissioner';

    representatives.sort(function (a, b) {
      var x = order.indexOf(a['elected_office']),
          y = order.indexOf(b['elected_office']);
      if (x < y) {
        return -1;
      }
      else if (x > y) {
        return 1;
      }
      else if (a['last_name'] < b['last_name']) {
        return -1;
      }
      else {
        return 1;
      }
    });

    var $representatives = $('<div id="representatives"></div>'), $row;

    var i = 0;
    $.each(representatives, function (j, object) {
      if (object['elected_office'] && object['related']['representative_set_url'].indexOf('/campaign-set-') === -1) {
        if (i % 6 == 0) {
          $row = $('<div class="row"></div>');
          $representatives.append($row);
        }
        else if (i % 3 == 0) {
          $row.append('<div class="clearfix visible-sm"></div>')
        }
        else if (i % 2 == 0) {
          $row.append('<div class="clearfix visible-xs"></div>')
        }
        $row.append($(representativeTemplate(object)));
        i++;
      }
    });

    $('#representatives').replaceWith($representatives);

    $('#representatives').imagesLoaded().progress(function (instance, image) {
      if (!image.isLoaded) {
        $(image.img).attr('src', '/static/img/silhouette.png');
      }
    });
  });
}

function initMap() {
  function processAddress() {
    $('.alert').hide();
    $('#addresses').empty();

    geocoder.geocode({address: $('#address').val(), region: 'ca', language: gettext('en')}, function (results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        if (results.length > 1) {
            $('#addresses').append('<option>' + gettext('Select your address') + '</option>');
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

  var geocoder = new google.maps.Geocoder(),
      map,
      marker,
      featureGroup,
      representativeTemplate = _.template( // This is the only underscore dependency.
        '<div class="col-xs-6 col-sm-4 col-md-2 representative">' +
          '<div class="avatar" style="background-image: url(<% if (photo_url) { %><%= photo_url %><% } else { %>/static/img/silhouette.png<% } %>)"></div> ' +
          '<p><% if (party_name) { %><%= party_name %><% } %> ' + '<%= elected_office %> ' +
          '<strong><% if (url) { %><a href="<%= url %>"><%= name %></a><% } else { %><%= name %><% } %></strong></p> ' +
          '<p class="district-name"><%= district_name %> <button type="button" class="btn btn-default btn-xs shape" data-url="<%= related.boundary_url %>">' + gettext('Map') + '</button></p> ' +
          '<p><% if (email) { %><a href="mailto:<%= email %>">' + gettext('Email') + ' <%= first_name %></a><% } %></p> ' +
        '</div>'
      );

  var latlng = L.latLng(45.444369, -75.693832), // 24 Sussex Drive, Ottawa
      index = window.location.href.indexOf('#'),
      anchor;

  // Create the map, marker and feature group.
  map = L.map('map', {
    center: latlng,
    layers: [
      L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        id: 'mapbox/streets-v11',
        accessToken: 'pk.eyJ1IjoianBtY2tpbm5leTIiLCJhIjoiY2p1M2Fzbm5pMGwzZTQ0bnl0ZDRrdHA3dyJ9.vtQ-f6tJQ3tYJc08ok03lQ'
      })
    ],
    maxZoom: 17,
    zoom: 13,
    scrollWheelZoom: false,
    touchZoom: false
  });
  map.attributionControl.setPrefix(false);
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

    getBoundaryShape($(this).data('url')).then(function (response) {
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
}
