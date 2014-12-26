$(function () {
  $.getJSON('http://represent.opennorth.ca/boundary-sets/?limit=0', function (data) {
    var boundary_sets = {}
      , key_map = {
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
        '/representative-sets/house-of-commons/': 'Canada',
        '/representative-sets/grande-prairie-city-council/': 'AB',
        '/representative-sets/lambton-county-council/': 'ON',
        '/representative-sets/lasalle-town-council/': 'ON',
        '/representative-sets/oshawa-city-council/': 'ON',
        '/representative-sets/peel-regional-council/': 'ON',
        '/representative-sets/waterloo-regional-council/': 'ON',
        '/representative-sets/abbotsford-city-council/': 'BC',
        '/representative-sets/burnaby-city-council/': 'BC',
        '/representative-sets/coquitlam-city-council/': 'BC',
        '/representative-sets/kelowna-city-council/': 'BC',
        '/representative-sets/langley-city-council/': 'BC',
        '/representative-sets/richmond-city-council/': 'BC',
        '/representative-sets/saanich-district-council/': 'BC',
        '/representative-sets/surrey-city-council/': 'BC',
        '/representative-sets/vancouver-city-council/': 'BC',
        '/representative-sets/victoria-city-council/': 'BC',
      }, provinces_key = gettext('Provincial legislatures');

    $.each(data.objects, function (i, boundary_set) {
      boundary_sets[boundary_set.url] = boundary_set.domain.split(', ')[1];
    });

    $.getJSON('http://represent.opennorth.ca/representative-sets/?limit=0', function (data) {
      var representative_sets = {'Canada': ['<li><a href="http://represent.opennorth.ca.s3.amazonaws.com/csv/complete.csv">' + gettext('All elected officials') + '</a></li>']}
        , keys = []
        , key
        , i
        , l
        , j
        , m
        , list
        , $ul;

      $.each(data.objects, function (i, representative_set) {
        key = boundary_sets[representative_set.related.boundary_set_url];
        if (!key) {
          if (/Assembl/.test(representative_set.name)) {
            key = provinces_key;
          }
          else {
            key = uncategorized_map[representative_set.url] || gettext('Uncategorized');
          }
        }
        if (!representative_sets[key]) {
          representative_sets[key] = [];
        }
        representative_sets[key].push('<li><a href="http://represent.opennorth.ca.s3.amazonaws.com/csv/' + representative_set.related.representatives_url.split('/')[2] + '.csv">' + representative_set.name + '</a></li>');
      });

      for (key in representative_sets) {
        if (representative_sets.hasOwnProperty(key)) {
          keys.push(key);
        }
      }

      $('#loading').remove();

      keys.sort();
      keys.splice($.inArray('Canada', keys), 1);
      keys.splice($.inArray(provinces_key, keys), 1);
      keys.unshift(provinces_key);
      keys.unshift('Canada');

      for (i = 0, l = keys.length; i < l; i++) {
        key = keys[i];
        list = representative_sets[key];
        list.sort();

        if (key != 'Canada') {
          $('#downloads').append('<h2>' + (key_map[key] || key) + '</h2>');
        }
        $ul = $('<ul></ul>');
        for (j = 0, m = list.length; j < m; j++) {
          $ul.append($(list[j]));
        }
        $('#downloads').append($ul);
      }
    });
  });
});
