part = 'rating-score-'
comment_number = 1

function plusRating(obj)
{
    var ratingId = obj.id;
    ratingId = ratingId.slice(5);
    var fullId = part + ratingId;
    var rating = document.getElementById(fullId).innerHTML;
    rating = parseInt(rating);
    rating += 1;
    document.getElementById(fullId).innerHTML = rating;
    return
}

function minusRating(obj)
{
    var ratingId = obj.id;
    ratingId = ratingId.slice(6);
    var fullId = part + ratingId;
    var rating = document.getElementById(fullId).innerHTML;
    rating = parseInt(rating);
    rating -= 1;
    document.getElementById(fullId).innerHTML = rating;
}

