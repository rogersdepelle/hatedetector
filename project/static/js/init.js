$(document).ready(function(){
    $('.modal').modal();
    $(".button-collapse").sideNav();
    $('select').material_select();
    $('.collapsible').collapsible();
    $('#card1').height($('#card2').height());
    $('#card3').height($('#card4').height());
});

$( window ).resize(function() {
    $('#card1').height($('#card2').height());
    $('#card3').height($('#card4').height());
});
