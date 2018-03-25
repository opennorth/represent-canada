$(function () {
  $.getJSON('https://represent.opennorth.ca/boundary-sets/?limit=0', function (data) {
    var boundary_sets = {}
      , provinces_key = gettext('Provincial legislatures')
      , iterations = {
          'elections': 'Candidates'
        , 'representative-sets': 'Representatives'
      }, key_map = {
          'NL': gettext('Newfoundland and Labrador councils')
        , 'PE': gettext('Prince Edward Island councils')
        , 'NS': gettext('Nova Scotia councils')
        , 'NB': gettext('New Brunswick councils')
        , 'QC': gettext('Quebec councils')
        , 'ON': gettext('Ontario councils')
        , 'MB': gettext('Manitoba councils')
        , 'SK': gettext('Saskatchewan councils')
        , 'AB': gettext('Alberta councils')
        , 'BC': gettext('British Columbia councils')
        , 'YT': gettext('Yukon councils')
        , 'NT': gettext('Northwest Territories councils')
        , 'NU': gettext('Nunavut councils')
      }, uncategorized_map = {
          '/elections/house-of-commons/': 'Canada'
        , '/representative-sets/house-of-commons/': 'Canada'
        , '/representative-sets/conseil-municipal-de-montreal/': 'QC'
        , '/representative-sets/grande-prairie-city-council/': 'AB'
        , '/representative-sets/lethbridge-city-council/': 'AB'
        // Ontario
        , '/representative-sets/georgina-town-council/': 'ON'
        , '/representative-sets/lambton-county-council/': 'ON'
        , '/representative-sets/lasalle-town-council/': 'ON'
        , '/representative-sets/niagara-regional-council/': 'ON'
        , '/representative-sets/oshawa-city-council/': 'ON'
        , '/representative-sets/peel-regional-council/': 'ON'
        , '/representative-sets/waterloo-regional-council/': 'ON'
        , '/representative-sets/whitchurch-stouffville-town-council/': 'ON'
        , '/representative-sets/uxbridge-township-council/': 'ON'
        // British Columbia
        , '/representative-sets/abbotsford-city-council/': 'BC'
        , '/representative-sets/burnaby-city-council/': 'BC'
        , '/representative-sets/coquitlam-city-council/': 'BC'
        , '/representative-sets/kelowna-city-council/': 'BC'
        , '/representative-sets/langley-township-council/': 'BC'
        , '/representative-sets/langley-city-council/': 'BC'
        , '/representative-sets/richmond-city-council/': 'BC'
        , '/representative-sets/saanich-district-council/': 'BC'
        , '/representative-sets/surrey-city-council/': 'BC'
        , '/representative-sets/vancouver-city-council/': 'BC'
        , '/representative-sets/victoria-city-council/': 'BC'
      };

    $.each(data.objects, function (i, boundary_set) {
      boundary_sets[boundary_set.url] = boundary_set.domain.split(', ')[1];
    });

    $.each(iterations, function (endpoint, label) {
      var path = label.toLowerCase()
        , field = path + '_url';

      $.getJSON('https://represent.opennorth.ca/' + endpoint + '/?limit=0', function (data) {
        var sets = {}
          , keys = []
          , key
          , i
          , l
          , j
          , m
          , list
          , $ul;

        if (label === 'Representatives') {
          sets['Canada'] = ['<li><a href="http://represent.opennorth.ca.s3.amazonaws.com/csv/' + path + '/complete.csv">' + gettext('All elected officials') + '</a></li>'];
        }

        $.each(data.objects, function (i, set) {
          var basename;

          if (set.url.indexOf('/campaign-set-') === -1 && set.url.indexOf('-municipal-councils') === -1) {
            key = boundary_sets[set.related.boundary_set_url];
            if (!key) {
              if (/Assembl/.test(set.name)) {
                key = provinces_key;
              }
              else {
                key = uncategorized_map[set.url] || gettext('Uncategorized');
              }
            }
            if (!sets[key]) {
              sets[key] = [];
            }
            basename = set.related[field].split('/')[2];
            // Exception.
            if (field == 'candidates_url' && basename == 'legislative-assembly-of-british-columbia') {
              basename = 'bc-legislature';
            }
            else if (field == 'candidates_url' && basename == 'legislative-assembly-of-ontario-2018') {
              basename = 'ontario-legislature';
            }
            sets[key].push('<li><a href="http://represent.opennorth.ca.s3.amazonaws.com/csv/' + path + '/' + basename + '.csv">' + set.name + '</a></li>');
          }
        });

        for (key in sets) {
          if (sets.hasOwnProperty(key)) {
            keys.push(key);
          }
        }

        keys.sort();
        $.each([provinces_key, 'Canada'], function (i, key) {
          var index = $.inArray(key, keys);
          if (index > 0) {
            keys.splice(index, 1);
            keys.unshift(key);
          }
        });

        $('#downloads').append('<h2>' + gettext(label) + '</h2>');
        for (i = 0, l = keys.length; i < l; i++) {
          key = keys[i];
          console.log(key);
          console.log(sets);
          list = sets[key];
          list.sort();

          if (key != 'Canada') {
            $('#downloads').append('<h3>' + (key_map[key] || key) + '</h2>');
          }
          $ul = $('<ul></ul>');
          for (j = 0, m = list.length; j < m; j++) {
            $ul.append($(list[j]));
          }
          $('#downloads').append($ul);
        }
      });
    });

    $('#loading').remove();
  });
});
