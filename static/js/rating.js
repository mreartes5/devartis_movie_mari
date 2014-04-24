$(document).ready(function (data) {
    $('#rank').click(function () {
        var movie_id;
        movie_id = $(this).attr("data-movie_id");
        $.post('/movie/' + movie_id + "/add-rating/", {value: $("#id_value").val()}, function (data) {
            $('#votes').text("Votes: " + data['votes_count']);
            $('#rating').text("Rating: " + data['new_rating']);
            $('#rank').text("Change rank");
            $('#last_rating').text("Your last rating: " + data['user_rating_for_movie'])
        });
    });


});