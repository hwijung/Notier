
$(document).ready( function()
{
	var btnCreateEntry = $("#id_btn_create_entry");

	btnCreateEntry.click( function (event ) {
		document.location.href = '/save'; 
	});
	
	// Activate button clicked
	$(".dropdown-menu li a").click(function() {
	
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
		            	    		
		    		if ( $("#monitoring_entries tbody tr").length == 0 ) {
		    			$("#monitoring_entries").remove();
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
