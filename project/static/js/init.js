$('.button-collapse').sideNav({
    menuWidth: 200,
    edge: 'left',
    closeOnClick: true
});

$(document).ready(function(){
    $('.modal-trigger').leanModal();
    $('select').material_select();
    $(".delete_item").click(function(){
      if(confirm("Are you sure you want to permanently delete this item?")){
        window.location.href = $(this).data('url')
      }
    });
});
