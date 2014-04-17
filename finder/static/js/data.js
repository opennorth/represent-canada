$(function () {
  $.getJSON('http://represent.opennorth.ca/boundary-sets/?limit=0', function (data) {
    var boundary_sets = {}
      , key_map = {
        'NL': 'Newfoundland and Labrador councils'
      , 'PE': 'Prince Edward Island councils'
      , 'NS': 'Nova Scotia councils'
      , 'NB': 'New Brunswick councils'
      , 'QC': 'Quebec councils'
      , 'ON': 'Ontario councils'
      , 'MB': 'Manitoba councils'
      , 'SK': 'Saskatchewan councils'
      , 'AB': 'Alberta councils'
      , 'BC': 'British Columbia councils'
      , 'YT': 'Yukon councils'
      , 'NT': 'Northwest Territories councils'
      , 'NU': 'Nunavut councils'
      }, uncategorized_map = {
        '/representative-sets/house-of-commons/': 'Canada',
        '/representative-sets/grande-prairie-city-council/': 'AB',
        '/representative-sets/lambton-county-council/': 'ON',
        '/representative-sets/lasalle-town-council/': 'ON',
        '/representative-sets/peel-regional-council/': 'ON',
        '/representative-sets/vancouver-city-council/': 'BC',
        '/representative-sets/victoria-city-council/': 'BC',
      };

    $.each(data.objects, function (i, boundary_set) {
      boundary_sets[boundary_set.url] = boundary_set.domain.split(', ')[1];
    });

    $.getJSON('http://represent.opennorth.ca/representative-sets/?limit=0', function (data) {
      var representative_sets = {'Canada': ['<li><a href="http://represent.opennorth.ca.s3.amazonaws.com/csv/complete.csv">All elected officials</a></li>']}
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
            key = 'Provincial legislatures';
          }
          else {
            key = uncategorized_map[representative_set.url] || 'Uncategorized';
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
      keys.splice($.inArray('Provincial legislatures', keys), 1);
      keys.unshift('Provincial legislatures');
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
