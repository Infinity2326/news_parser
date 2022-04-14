rating = 0;

function plusRating()
{
    rating = rating + 1
    document.getElementById('rating_score').innerHTML=rating;
}

function minusRating()
{
    rating = rating - 1
    document.getElementById('rating_score').innerHTML=rating;
}