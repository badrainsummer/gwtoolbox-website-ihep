var cor_err={"M1":"dm1","M2":"dm2","z":"dz","s1":"ds1","d2":"ds2","D":"dD","f":"df","Amp":"dAmp","μ":"dμ","Μ":"dΜ","D":"dD"}
function updateform() {
        // first collapse/uncollapse
        $('#selfCosmos').toggle($('select#cosmo_model').val()=='FlatLambdaCDM');
        $('#BBHmodel').toggle($('select#event_type').val()=='bhbh');
        $('#DNSmodel').toggle($('select#event_type').val()=='nsns');
        $('#BHNSmodel').toggle($('select#event_type').val()=='bhns');
        $('#mbhbmodel').toggle($('select#sourcetype_mHz').val()=='1');
        $('#gwdmodel').toggle($('select#sourcetype_mHz').val()=='2');
        $('#emrimodel').toggle($('select#sourcetype_mHz').val()=='3');
        $('#tablepar').toggle($('input#output2').prop('checked'));
        $('#tablepar2').toggle($('input#output3').prop('checked'));
        $('#tablehist').toggle($('input#output3').prop('checked'));
        $('#tableplot').toggle($('input#output4').prop('checked'));
        $('#ifYesDet').toggle($('select#detector_type').val()=='ligo-like');
        $('#iflisalike').toggle($('select#detector_name').val()=='-1');
        $('#ifExisting').toggle($('select#plan').val()<0);
        $('#ifFuture').toggle($('select#plan').val()==0);
        $('#ifindividalBH').toggle($('select#IDsource').val()=='-1');
        $('#ifSGWB').toggle($('select#IDsource').val()==0);
        $('#ifSens').toggle($('select#IDsource').val()=='1');
        $('#if_with_errors').toggle($('input#output3').prop('checked'));
        $('#SMBHB_columns').toggle($('select#sourcetype_mHz').val()=='1');
        $('#GWD_columns').toggle($('select#sourcetype_mHz').val()=='2');
        $('#EMRIs_columns').toggle($('select#sourcetype_mHz').val()=='3');
	if (Number($('#obs_time').val())>3650 || Number($('#obs_time').val())<37){
		alert("Observation duration out of range, try within 0.5-10 years")
	}
        $('#warning').toggle($('select#sourcetype_mHz').val()=='3');
        $('#warning_M11').toggle($('select#emri_pop').val()=='11');
	checkinput();
}


// do it once initially
updateform();
function checkinput() {
	if (!($('input#det_arm').val()>2.5e8) || !($('input#det_arm').val()<5e10)){
        	alert("We limit the arm length of LISA in between 2.5e8 and 5e10.")
               	document.getElementById("det_arm").value='2.5e9';    }
        if (!($('input#det_laser_power').val()>0)) {
		alert("The laser power needs to be positive!")
		document.getElementById("det_laser_power").value='2.0';
	}
	if (!($('input#det_dia').val()>0)){
		alert("The telescope diameter needs to be positive!")
		document.getElementById("det_dia").value='0.3';
	}
	if (!($('input#Sacc0').val()>1e-49) || !($('input#Sacc0').val()<1e-39)){
		alert("We limit Sacc0 in between 1e-49 and 1e-39.")
		document.getElementById("Sacc0").value='3.9e-44';
	}
	
	if (!($('input#Sops').val()>1e-43) || !($('input#Sops').val()<1e-33)){
		alert("We limit Sops in between 1e-43 and 1e-33.")
		document.getElementById("Sops").value='5.3e-38';
	}
		
	if (!($('input#Sopo0').val()>1e-43) || !($('input#Sopo0').val()<1e-33)){
		alert("We limit Sopo0 in between 1e-43 and 1e-33.")
		document.getElementById("Sopo0").value='2.81e-38';
	}
	if (!($('input#signal_to_noise').val()>=0)){
		alert("snr must be non-negative.");
		document.getElementById("signal_to_noise").value='8';
		}

        if ($('select#sourcetype_mHz').val()=='2'){
		if (!($('input#obs_time').val()>=0)){
			alert("obs_time must be non-negative.");
			document.getElementById("obs_time").value='365';
			}
	}else{
		if (!($('input#obs_time').val()>182.5) || !($('input#obs_time').val()<1825)){
                        alert("obs_time are limited from 0.5 yr to 5 yr for this population.");
                        document.getElementById("obs_time").value='365';
                        }
	}
	if (!($('input#H0').val()>60)||!($('input#H0').val()<80)){ 
		alert("We constrain the range of H0 in 60-80.");
		document.getElementById("H0").value='70';
		}
	if (!($('input#omega').val()>0.1)||!($('input#omega').val()<0.9)){
		alert("We constrain the range of omega in 0.1-0.9");
		document.getElementById("omega").value='0.3';
		}
	if (!($('input#Tcmb').val()>2) || !($('input#Tcmb').val()<4 )){
		alert("We constrain the range of Tcmb in 2-4");
		document.getElementById("Tcmb").value='2.725';
		}
	if (!($('input#output_size_table').val()<=100 )|| !($('input#output_size_table').val()>0)){
		alert("We constrain the range of max_event in 0-100. For a larger catalogue, please run the pacakge in your local.")
		document.getElementById("output_size_table").value='100';	
		}	
	if (!($('input#output_size_table2').val()<=50 )|| !($('input#output_size_table2').val()>0)){
		alert("We constrain the range of max_event in 0-50. For a larger catalogue, please run the pacakge in your local.")
		document.getElementById("output_size_table2").value='10';	
		}	
}
var busy = false;
function submitform() {
	// disable submit button to prevent repetitive activation
	// TODO: choose a nicer layout framework because the current one doesn't support the disabed rendering
	// TODO: handle errors encoded as a msg in the python response (i.e. expected errors)
        //alert("I'm doint the job");	
	let form = $('form#setup');
	form.prop('disabled', true);
    jump("status")   
        $('#status').html("<img src='/images/Ellipsis-1.4s-50px.gif' />");
	// submit data
        // clear potential old results
        $('#total').empty()
		$('#snr').empty()
        $('#sensitivity.plot').empty()
        $('#plot.plot').empty()
        $('#table').empty();
        //working on new results
	const data = form.serialize();
	const url = form.attr('action');
	$.post(url, data)
		.done(function(data) {
			// when done, process data
			console.log(data);

			if (!data.success) {
                $('#status').html("Waiting for your input ...");
				alert("Request successful but server replied with AN error: "+data.msg);
				return;
			}

			if (data.total) {
				$('#total').text(Math.round(data['total']));
				// $('#snr').text(data['snr']);
				make_sensitivity_plot(data);
				make_vs_plot(data);
				plot_options_changed()
				make_table(data);
				$('#status').html(" ");
			}
			if (data.snr) {
				$('#snr').text(data['snr']);
				make_sensitivity_plot(data);
				$('#status').html(" ");
			}
		})
		.fail(function() {
			// TODO: build nicer error into html
			$('#status').html("Waiting for your input ...");
			alert("Oops, something went wrong!");
		})
		.always(function() {	
			// always re-enable all form elements
			form.prop('disabled', false);
		});

	// supress normal form handler
	return false;
}


function make_sensitivity_plot(data) {
	// prepare a trace for the selected detector type
	let trace = {
		type: 'scattergl',
		x: data['sensitivity'][0],
		y: data['sensitivity'][1],
		mode: 'lines',
		//name: data['config']['detector_type']
                name: 'LISA'
	};
	let plotdata = [trace];
	
	
	// prepare a trace for the default comparable detector
	// TODO; untested because this part of the server code doesn't work
	//if (data['config']['detector_type'].endsWith('-like')) {
	//	let default_trace = {
	//		x: data['default_sensitivity'][0],
	//		y: data['default_sensitivity'][1],
	//		mode: 'line',
	//		name: data['config']['detector_type'].slice(0, -5)
	//	}
	//	plotdata.push(default_trace);
	//}

	// define a layout
	let layout = {
                width: 550,
                height: 350,
		title: "Sensitivity curve",
		xaxis: {
			type: 'log',
			autorange: true,
            exponentformat:"power",
            title: "Frequency (Hz)"
		},
		yaxis: {
			type: 'log',
			autorange: true,
            exponentformat:"power",
            title: "Strain (1/√Hz)"
		}
	};

	// Create or update the plot in the html
	Plotly.newPlot($('#sensitivity.plot').get(0), plotdata, layout);
    $('#downloadsenscurve').toggle()
}
//function make_vs_plot(){
//    plot_options_changed()
//}
function make_vs_plot(data) {
	form = $('form#plot_options');

	// extra the available quantities from the data
	let variables = [];
	if (data['events'] && data['events'].length > 0) {
		// quite arbitrarily take the keys from the first one
		variables = Object.keys(data['events'][0]);
	}

	// clear current select options
	form.find('#xvar').empty();
	form.find('#yvar').empty();
	form.find('#xerror').empty();
	form.find('#yerror').empty();
	
	form.find('#xerror').append($('<option value="none">None</option>'));
	form.find('#yerror').append($('<option value="none">None</option>'));
	
	for (const v of variables) {
		// create an option tag
		let new_option = $('<option>');
		new_option.val(v);
		new_option.text(v);
		// append a clone to both dropdowns
		form.find('#xvar').append(new_option.clone());
		form.find('#yvar').append(new_option.clone());
		//form.find('#xerror').append(new_option.clone());
		//form.find('#yerror').append(new_option.clone());
	}
	
	// save data for later
	window.data = data;
}

function plot_options_changed() {
	console.log('plot options changed');
	form = $('form#plot_options');
	let xvar = form.find('#xvar').val();
	let yvar = form.find('#yvar').val();
        if (form.find('#x_error_option').prop('checked')){
                xerror = cor_err[xvar]} else {
                xerror = 'none'}
        if (form.find('#y_error_option').prop('checked')){
                yerror = cor_err[yvar]} else {
                yerror = 'none'}
	//let xerror = form.find('#xerror').val();
	//let yerror = form.find('#yerror').val();
	
//	if (xvar == yvar) {
//		// TODO: better message
//		console.log('Cannot plot same variable vs itself');
//		return;
//	}

	// extract series
    let plotdata=[]
    let layout={}
	let xdata = []
	let ydata = []
	let xerrordata = []
	let yerrordata = []

    if (xvar!=yvar){
        for (i in window.data.events) {
            xdata.push(window.data.events[i][xvar]);
            ydata.push(window.data.events[i][yvar]);
            if (xerror != 'none') xerrordata.push(window.data.events[i][xerror]);
            if (yerror != 'none') yerrordata.push(window.data.events[i][yerror]);
        }
	// prep data for plot
		let trace = {
			type: 'scattergl',
			x: xdata,
			y: ydata,
			mode: 'markers'
		};
		// add error bars
		if (xerror != 'none') {
			trace['error_x'] = {
				type: 'data',
				array: xerrordata,
				visible: true
			}
		}
		if (yerror != 'none') {
			trace['error_y'] = {
				type: 'data',
				array: yerrordata,
				visible: true
			}
		}
		try{
            plotdata = [trace];
        } catch(err){
        alert(err.message)
        }
		// define a layout
		layout = {
            autosize: false,
            width: 550,
            height: 350,
			title: xvar + " vs. " + yvar,
			xaxis: {
				type: form.find('#xlog').prop('checked') ? 'log' : 'linear',
				autorange: true,
				title: xvar,
                exponentformat:"power"
			},
			yaxis: {
				type: form.find('#ylog').prop('checked') ? 'log' : 'linear',
				autorange: true,
				title: yvar,
                exponentformat:"power"
			}
		};
	} else {
         for (i in window.data.events) {
            if (form.find('#xlog').prop('checked')){
                xdata.push(Math.log10(window.data.events[i][xvar]));
            } else {
                xdata.push(window.data.events[i][xvar]);
            }
            //ydata.push(window.data.events[i][yvar]);
            if (xerror != 'none') xerrordata.push(window.data.events[i][xerror]);
            //if (yerror != 'none') yerrordata.push(window.data.events[i][yerror]);
        }   
		let trace = {
            x: xdata,
            type: 'histogram'
            //mode: 'markers'
        };
        try{
            plotdata = [trace];
        } catch(err){
        alert(err.message)
        }
		//let plotdata = [trace];
		layout = {
            autosize: false,
            width: 550,
            height: 350,
            title: form.find('#xlog').prop('checked') ? 'log '+xvar+" histrogram" : xvar + " histogram", 
            xaxis: {
                //type: form.find('#xlog').prop('checked') ? 'log' : 'linear',
                type: 'linear', 
                autorange: true,
                exponentformat:"power",
                title: form.find('#xlog').prop('checked') ? 'log '+xvar : xvar
            }, 
            yaxis: {
				type: form.find('#ylog').prop('checked') ? 'log' : 'linear',
				autorange: true,
                exponentformat:"power",
				title: yvar
			}
        };
    }

//	
//		// Create or update the plot in the html
//    alert("data?")
    try{
        Plotly.newPlot($('#plot.plot').get(0), plotdata, layout);
    } catch(err){
        alert(err.message)
    }
}

function make_table(data) {
	// clear potential old table
	$('#table').empty();

	// early abort if there are 0 rows
	if (data.events.length == 0) {
		return;
	}

	// create the table in memory
	let table = $('<table>');
	// build header row:
	let header = $('<tr>');
	for (let v in data.events[0]) {
		let th = $('<th>');
		th.text(v);
		header.append(th);
	}
	table.append(header);
	// build data rows:
	for (let row of data.events) {
		let tr = $('<tr>');
		for (let v in row) {
			let td = $('<td>');
			let val = row[v];
                        if (typeof val == 'number') {
			        let rounded = val.toPrecision(2);
			        if (val < 0.01 || val >= 100) {
				        rounded = Number.parseFloat(rounded).toExponential();
			        }
                                td.text(rounded);
                        } else {
			        td=val;
                        }
			tr.append(td);
		}
		table.append(tr);
	}
	// put table in dom
	$('#downloadtab').toggle()    
	$('#table').append(table);
	
}
function savetable(){
    //alert("saving! round:2")
    //form = $('form#savetab');
    try {
        jsondata=window.data.events
        //jsondata=[]
        var file =new Blob([JSON.stringify(jsondata)], {type: 'text/plain'});
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

function savecurve(){
    try {
        data=window.data.sensitivity
        jsondata={"frequency":data[0],"TDI-X":data[1]}
        var file =new Blob([JSON.stringify(jsondata)], {type: 'text/plain'});
        var url = window.URL.createObjectURL(file);
        var a = document.createElement('a');
        //a.style.display = 'none';
        a.href = url;
        // the filename you want
        //a.download = form.find('#filename').val();
        a.download = $('input#filename_senscurve').val()+".json"
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        //alert("saved! lalala")
    } catch (err) {
        alert(err.message)
    }
}

function jump(h){
    var top = document.getElementById(h).offsetTop;
    window.scrollTo(0, top);
}
