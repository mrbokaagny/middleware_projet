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

        if($('#card-to-load-admin-content-page__ .modal-to-update-data').hasClass('active-modal')){
            $('#card-to-load-admin-content-page__ .modal-to-update-data').removeClass('active-modal')
        }

    })

    $('#card-to-load-admin-content-page__').on('click' , '.btn-to-close-modal-create' , function(e){
        $('#card-to-load-admin-content-page__ .overlay-card-to-create').removeClass('active_modal_create')
    })

    $('#card-to-load-admin-content-page__').on('click' , '.btn-fade-modal-update' , function(e){
        $('#card-to-load-admin-content-page__ .modal-to-update-data').addClass('active-modal')
    })


  

   
    setTimeout(() => {
        document.querySelectorAll(".flash-message").forEach(msg => msg.remove());
    }, 3000);

})(jQuery)