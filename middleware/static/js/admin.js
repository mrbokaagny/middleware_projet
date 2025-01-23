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

    $('#card-to-load-admin-content-page__').on('click' , '.btn-to-active-modal-create' , function(e){
        $('#card-to-load-admin-content-page__ .overlay-card-to-create').addClass('active_modal_create')
    })

    $('#card-to-load-admin-content-page__').on('click' , '.btn-to-close-modal-create' , function(e){
        $('#card-to-load-admin-content-page__ .overlay-card-to-create').removeClass('active_modal_create')
    })

  

   


})(jQuery)