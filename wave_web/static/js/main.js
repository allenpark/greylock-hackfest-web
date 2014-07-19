$(document).ready(function() {
    $('.message-input').bind('input', function(e) {
        var text = $('.message-input').val();
        if (text === '') {
            text = '&nbsp;';
        }
        $('.preview').html(text);
    });
});
