(function($){

    setTimeout(() => {
        document.querySelectorAll(".flash-message").forEach(msg => msg.remove());
    }, 3000);

})(jQuery)