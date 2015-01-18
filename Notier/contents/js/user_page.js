
$(document).ready( function()
{
	var btnCreateEntry = $("#id_btn_create_entry");

	btnCreateEntry.click( function (event ) {
		document.location.href = '/entry/save'; 
	});
	
	// Activate button clicked
	$("#id_entry_btn_group ul li a").click(function() {
		entry_name = $(this).attr("name");
		id_of_clicked_button = "#id_btn_activate_" + entry_name;
		$(id_of_clicked_button).contents().get(0).nodeValue = $(this).text() + " ";

		if ( $(this).text() == "Activate" ) {
			$(id_of_clicked_button).addClass( "btn-success" );
			$(id_of_clicked_button).removeClass( "btn-danger" );
			activateEntry( entry_name, "ON" );
		} else {
			$(id_of_clicked_button).addClass( "btn-danger" );
			$(id_of_clicked_button).removeClass( "btn-success" );	
			activateEntry( entry_name, "OFF" );
		}
	} );
} );

function activateEntry( entry_name, on ) {
	var requestURL = "/entry/activate/";
	var jqXHR = $.ajax ( {
		xhr: function () {
			var xhrobj = $.ajaxSettings.xhr();
			return xhrobj;
		},
		url: requestURL,
		headers: { "X-CSRFToken": getCookie('csrftoken') },
		type: "POST",
		cache: false,
		data: { entry_name: entry_name, activate: on },
		success: function( result ) {
			return jQuery.parseJSON( result );
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
