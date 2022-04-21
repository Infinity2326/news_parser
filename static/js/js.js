part = 'rating-score-'

function plusRating(obj)
{
    var ratingId = obj.id
    ratingId = ratingId.slice(5)
    var fullId = part + ratingId;
    var rating = document.getElementById(fullId).innerHTML;
    rating = parseInt(rating);
    rating += 1;
    document.getElementById(fullId).innerHTML=rating;
}

function minusRating(obj)
{
    var ratingId = obj.id
    ratingId = ratingId.slice(7)
    var fullId = part + ratingId;
    var rating = document.getElementById(fullId).innerHTML;
    rating = parseInt(rating);
    rating -= 1;
    document.getElementById(fullId).innerHTML=rating;
}


