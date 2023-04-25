$('.vertical-menu a').click(function(){
    $(this).addClass('active').siblings().removeClass('active');
    });


$('button').on('click', function() {
    $('body').css('background', '#ccc');
});

function toggleFav(btn) {
    btn.classList.toggle('active');
  }