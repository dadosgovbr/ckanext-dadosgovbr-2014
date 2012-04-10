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

  var size = parseFloat(document.body.style.fontSize);

  if (((size <= 1.6) && (multiplier < 0)) || ((size >= 0.5) && (multiplier > 0))){
    document.body.style.fontSize = size + (multiplier * 0.2) + "em";    
  }

}


