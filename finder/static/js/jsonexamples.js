function loadJSONExamples() {
    $('pre.loadjson').each(function() {
        var $el = $(this);
        if (!$el.html().length) {
            $.ajax({
                url: $el.data('url'),
                dataType: 'text',
                success: function(data) {
                    $el.html(formatJSON(data));
                }
            });
        }
    });
}