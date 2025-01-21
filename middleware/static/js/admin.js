(function($){

    $('#btn-active-right-overlay-card').click(function(e){
        e.preventDefault();
        $(".overlay-card-menu").toggleClass('active-rigth-card-menu')
    })

    $('#btn-toggle-web-side-menu').click(function(e){
        e.preventDefault();
        $('.web-left-card').toggleClass('active-toggle-web-side')
        $('.right-card').toggleClass('active-right-card')
    })

  

   


})(jQuery)