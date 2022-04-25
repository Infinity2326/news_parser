part = 'rating-score-'
comment_number = 0
parent_div = document.querySelector('.comment-section');

function plusRating(obj)
{
    var ratingId = obj.id;
    ratingId = ratingId.slice(5);
    var fullId = part + ratingId;
    var rating = document.getElementById(fullId).innerHTML;
    rating = parseInt(rating);
    rating += 1;
    document.getElementById(fullId).innerHTML = rating;
}

function minusRating(obj)
{
    var ratingId = obj.id;
    ratingId = ratingId.slice(7);
    var fullId = part + ratingId;
    var rating = document.getElementById(fullId).innerHTML;
    rating = parseInt(rating);
    rating -= 1;
    document.getElementById(fullId).innerHTML = rating;
}

function create_comment()
{
    var comment_author = document.getElementById("author").value;
    var comment_text = document.getElementById("comment").value;

    if (comment_author !== "" && comment_text !== "") {
        var div_author = document.createElement('div');
        var comment_id = 'comment-' + comment_number;
        div_author.id = comment_id;
        div_author.className = 'comment-author'
        parent_div.appendChild(div_author);
        document.getElementById(comment_id).innerHTML = comment_author;

        var div_text = document.createElement('div');
        comment_id = 'author-' + comment_number;
        div_text.id = comment_id;
        div_text.className = 'comment-text'
        parent_div.appendChild(div_text);
        document.getElementById(comment_id).innerHTML = comment_text;

        comment_number += 1
        document.getElementById("author").value = "";
        document.getElementById("comment").value = "";
        }
    else{
        alert("Please, input values")
    }

}
