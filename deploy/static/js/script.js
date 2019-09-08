$(function() {
    $('button').click(function() {
        var exp = $('#exp').val();
        $.ajax({
            url: 'http://localhost:5000/api',
            data: exp,
            type: 'POST',
            dataType: 'json',
            contentType: 'application/x-www-form-urlencoded',
            success: function(response) {
                console.log(response);
                $('#result').html(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
