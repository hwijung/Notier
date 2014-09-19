$(document).ready(function()
{
	var btnStartBeat = $("#id_btn_startbeat");
	var btnStopBeat = $("#id_btn_stopbeat");
		
	btnStartBeat.click( function( event ) {
		startBeat(true);
	} );
	
	btnStopBeat.click( function( event ) {
		startBeat(false);
	} );
});

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

function startBeat(start) {
	var requestURL = "/beat/";
	var formData = new FormData();
	
	formData.append ('start', start );
	
	var jqXHR = $.ajax ( {
		xhr: function () {
			var xhrobj = $.ajaxSettings.xhr();
			return xhrobj;
		},
		url: requestURL,
       headers: { "X-CSRFToken": getCookie('csrftoken') },		
       type: "POST",	
       contentType: false,
       processData: false,
       cache: false,
       data: formData,   
       success: function( data ) {
       	if ( data.result > 0 )
       		alert ("operation success!");
       	else {
       		alert ("operation failed.");	       		
       		}
        }        
	});
}
