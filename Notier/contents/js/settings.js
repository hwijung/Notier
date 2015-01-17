$(document).ready( function()
{
	
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
	
	
}