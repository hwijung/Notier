
$(document).ready( function()
{
	var btnBeat = $("#id_btn_beat");
	var btnCreateEntry = $("#id_btn_create_entry");
	
	btnBeat.click( function( event ) {
		toggleBeat();
	} );

	btnCreateEntry.click( function (event ) {
		document.location.href = '/save'; 
	});
} );

function toggleBeat() {
	var requestURL = "/beat/";
	var formData = new FormData();

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
       success: function( result ) {
    	   result = jQuery.parseJSON ( result );
    	   direction = ""
    	   if ( "ON" == $("#id_btn_beat").html() ) {
    		   direction = "OFF";
    	   } else {
    		   direction = "ON";   		   
    	   }
    	   
    	   show_message ( 'Notification', "Turned " + $("#id_btn_beat").html() )
    	   $("#id_btn_beat").html ( direction ); 
        }        
	});
}

function edit_click (clicked_id) {
	document.location.href = '/entry/' + clicked_id;
}

function delete_click( clicked_id ) {
	var result = confirm('Are you sure you want to do this?');
	
	if ( result ) {
		$.ajax({
			url: '/entry/' + clicked_id + '/',
			type: 'DELETE',
			beforeSend: function(xhr) {
				xhr.setRequestHeader("X-CSRFToken", $.cookie("csrftoken"));
		    },
		    success: function(result) {
		    	// Delete it from the table
		    	result = jQuery.parseJSON ( result );
		    	if ( result.result == "success" ) {
		    		$("#id_btn_edit_" + clicked_id ).parent().parent().remove();
		            	    		
		    		if ( $(".monitoring_entries tbody tr").length == 0 ) {
		    			$(".monitoring_entries").remove();
		    			$("#id_entry_list").append("<p>No monitoring site found.</p>");
	               	}
	           	}
		    }
		});
	}
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
