function show_message ( title, msg ) {
   				$("#id_notification_bar_title").html ( title );
   				$("#id_notification_bar_message").html ( msg );
   				$("#id_notification_bar").fadeIn ( 300, function () {
   					$("#id_notification_bar").fadeTo ( 2000, 0.9, function () {
   						$("#id_notification_bar").fadeOut ( 1000 ) ;  }  )  } );
   			}