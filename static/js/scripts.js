$("informlost]").submit(function(e){

	var $form = $(this);
	var $error = $form.find(".error");
    var data = $form.serialize();

    $ajax({
    	url: $(this).attr('action'),
    	type: "POST",
    	data: data,
    	dataType: "json",
    	success: function(data){
    		console.log(resp);
    		var element = document.getElementById("Lost");
            element.classList.add("success");
            element.innerHTML += '<div class="thanks">Thanks for Reporting. We will get back to you soon!</div>';
    	},
    	error: function(data){
    		console.log(resp);
    	}
    });

	e.preventDefault();
});
