$(document).ready( function()
{
	$(".btn-group ul li a").click(function() {
	
		$("#id_btn_activate").contents().get(0).nodeValue = $(this).text() + " ";
		
		if ( $(this).text() == "Activate" ) {
			$("#id_btn_activate").addClass( "btn-success" );
			$("#id_btn_activate").removeClass( "btn-danger" );
			toggleBeat( "ON" );
		} else {
			$("#id_btn_activate").addClass( "btn-danger" );
			$("#id_btn_activate").removeClass( "btn-success" );	
			toggleBeat( "OFF" );
		}
	});	
	
	$('#id_input_email').keyup ( function() {
		$("#id_btn_save").removeAttr( "disabled" );	
		$("#id_btn_save").addClass( "btn-success" );
	});	
	
	$('#id_btn_save').click( function() {
		var requestURL = window.location.pathname;
		var email = $('#id_input_email').val();
		var jqXHR = $.ajax ( {
			xhr: function () {
				var xhrobj = $.ajaxSettings.xhr();
				return xhrobj;
			},
			url: requestURL,
			headers: { "X-CSRFToken": getCookie('csrftoken') },
			type: "POST",
			cache: false,
			data: { email: email },
			success: function( result ) {
				$("#id_btn_save").attr( "disabled", true );	
				$("#id_btn_save").removeClass( "btn-success" );				
			}
		});		
	});
} );

function toggleBeat( on ) {
	var requestURL = "/beat/";
	var jqXHR = $.ajax ( {
		xhr: function () {
			var xhrobj = $.ajaxSettings.xhr();
			return xhrobj;
		}, 
		url: requestURL,
       headers: { "X-CSRFToken": getCookie('csrftoken') },		
       type: "POST",	
       cache: false,
       data: { direction: on },   
       success: function( result ) {
    	   result = jQuery.parseJSON ( result );
        }         
	});
}