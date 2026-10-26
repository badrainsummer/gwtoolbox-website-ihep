function updateform() {
	// first collapse/uncollapse
	//$('#BBHmodel').toggle($('select#event_type').val()=='bhbh');
	//$('#DNSsmodel').toggle($('select#event_type').val()=='nsns');
	//$('#BHNSsmodel').toggle($('select#event_type').val()=='bhns');
	//$('#mbhbmodel').toggle($('select#sourcetype_mHz').val()=='1');
	//$('#gwdmodel').toggle($('select#sourcetype_mHz').val()=='2');
	//$('#emrimodel').toggle($('select#sourcetype_mHz').val()=='3');
	//$('#tablepar').toggle($('input#output2').prop('checked'));
        //$('#tablepar2').toggle($('input#output3').prop('checked'));
	//$('#tablehist').toggle($('input#output3').prop('checked'));
	//$('#tableplot').toggle($('input#output4').prop('checked'));
	//$('#ifYesDet').toggle($('select#detector_type').val()=='ligo-like');
        //$('#iflisalike').toggle($('select#detector_name').val()=='-1');
        $('#ifExisting').toggle($('select#plan').val()<0);	
        $('#ifFuture').toggle($('select#plan').val()==0);
        $('#ifindividalBH').toggle($('select#IDsource').val()=='-1');
        $('#ifSGWB').toggle($('select#IDsource').val()==0); 
        $('#ifSens').toggle($('select#IDsource').val()=='1');
        $('#selfCosmos').toggle($('select#cosmology').val()=='FlatLambdaCDM');
}


// do it once initially
updateform();

var busy = false;
function submitform() {
	try {
		if (busy) {
			alert("Your previous calculation is not yet done. Please be patient...");
			return false;
		}
		busy = true;
		
		// post the form in an asynchronous ajax request
		const xhr = new XMLHttpRequest();
		const data = $('form').serialize();
		const url = $('form').attr('action');
//        $.post(url, data)
//		.done(function(data) {
//			// when done, process data
//			console.log(data);
//		})
//		.fail(function() {
//			// TODO: build nicer error into html
//			alert("Oops, something went wrong!");
//		})
//		.always(function() {
//			// always re-enable all form elements
//			form.prop('disabled', false);
//		});
		xhr.open("POST", url, true);
		xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
		xhr.send(data);
		
		// show a loading image and clear the output box
		$('#status').html("<img src='/images/Ellipsis-1.4s-50px.gif' />");
		$('#result').html("");

		// scroll to the output
		$("#status").parent().parent().get(0).scrollIntoView();

		// reset the recaptcha because each code is valid only once
		//update_captcha_token()

		// periodically check if the ajax call has some updates
		let timer = setInterval(function() {
			let data = xhr.responseText;
			$('#result').html(data);
			if (xhr.readyState == xhr.DONE) {
				clearInterval(timer);
				busy = false;
				$('#status').html("Done");
			}
		}, 100);
	}
	
	catch(e) {
		console.error(e)
	}
	// supress normal form handler
	return false
}

function update_captcha_token() {
	try {
		grecaptcha.ready(function() {
			grecaptcha.execute('6LchHMIUAAAAAGzHYwFRL6lW-9qqoMpiLMt52rz2', {action: 'earth'}).then(function(token) {
				$('#recaptcha').val(token);
			});
		});
	}
	catch(e) {
		
	}
}

function savetable(){
    alert("trying to save!")
    //form = $('form#savetab');
    //let data = $('form').serialize();

    try {
        //jsondata=window.data
        //jsondata=[]
        //var file =new Blob([JSON.stringify(jsondata)], {type: 'text/plain'});
        //var url = window.URL.createObjectURL(file);
        // VUC down here:
        //senscurve=$(input'#sens_freqs').val()
        //senscurve={"testing": 314}
        //var file =new Blob([JSON.stringify(senscurve)], {type: 'text/plain'});
        var file =new Blob(["hehehe"], {type: 'text/plain'});
        var url = window.URL.createObjectURL(file);
        var a = document.createElement('a');
        //a.style.display = 'none';
        a.href = url;
        // the filename you want
        //a.download = form.find('#filename').val();
        a.download = $('input#filename').val()+".json"
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        //alert("saved! lalala")
    } catch (err) {
        alert(err.message)
    }
}
