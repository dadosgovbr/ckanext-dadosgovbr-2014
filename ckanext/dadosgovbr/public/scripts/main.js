$(document).ready(function() {
    $('.dropdown-toggle').dropdown();
    $('.carousel').carousel();
    $('.myCarousel').carousel({
        interval: 2000
    })
    $('#top_apps_tabs').tab('show');
});

/*
* Redimensiona o texto das páginas
*/
function resizeText(multiplier) {
  if (document.body.style.fontSize == "") {
    document.body.style.fontSize = "1.0em";
  }
  document.body.style.fontSize = parseFloat(document.body.style.fontSize) + (multiplier * 0.2) + "em";
}


