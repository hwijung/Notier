function show_message ( title, msg ) {
   				$("#id_notification_bar_title").html ( title );
   				$("#id_notification_bar_message").html ( msg );
   				$("#id_notification_bar").fadeIn ( 300, function () {
   					$("#id_notification_bar").fadeTo ( 2000, 0.9, function () {
   						$("#id_notification_bar").fadeOut ( 1000 ) ;  }  )  } );
}


function getCookie(name) { 
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }  
    }
    return cookieValue;
}
