var btn = document.getElementById("theme-button");
var link = document.getElementById("theme-link");


function ChangeTheme()
{
    let lightTheme = "static/css/light-theme.css";
    let darkTheme = "static/css/dark-theme.css";

    var currTheme = link.getAttribute("href");

    if(currTheme == lightTheme)
    {
   	 currTheme = darkTheme;
   	 theme = "dark-theme.css";
    }
    else
    {
   	 currTheme = lightTheme;
   	 theme = "light-theme.css";
    }

    link.setAttribute("href", currTheme);

    sessionStorage.setItem("theme", theme);

}

$('.like, .dislike').on('click', function() {
    event.preventDefault();
    $('.active').removeClass('active');
    $(this).addClass('active');
});