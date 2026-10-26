//alert("I'm printing smth");
var cor_err={"D":"dD","m1":"dm1","m2":"dm2","χ":"dχ","z":"dz"}
function updateform() {
        // first collapse/uncollaps
        $('#selfCosmos').toggle($('select#cosmology').val()=='FlatLambdaCDM');
        $('#BBHmodel').toggle($('select#event_type').val()=='bhbh');
        $('#DNSmodel').toggle($('select#event_type').val()=='nsns');
        $('#BHNSmodel').toggle($('select#event_type').val()=='bhns');
//        $('#mbhbmodel').toggle($('select#sourcetype_mHz').val()=='1');
//        $('#gwdmodel').toggle($('select#sourcetype_mHz').val()=='2');
//        $('#emrimodel').toggle($('select#sourcetype_mHz').val()=='3');
        $('#tablepar').toggle($('input#output2').prop('checked'));
        $('#tablepar2').toggle($('input#output3').prop('checked'));
//        $('#tablehist').toggle($('input#output3').prop('checked'));
//        $('#tableplot').toggle($('input#output4').prop('checked'));
        $('#ifYesDetLigo').toggle($('select#detector_type').val()=='ligo-like');
        $('#ifYesDetET').toggle($('select#detector_type').val()=='et-like');
//        $('#iflisalike').toggle($('select#detector_name').val()=='-1');
//        $('#ifExisting').toggle($('select#plan').val()<0);
//        $('#ifFuture').toggle($('select#plan').val()==0);
//        $('#ifindividalBH').toggle($('select#IDsource').val()=='-1');
//        $('#ifSGWB').toggle($('select#IDsource').val()==0);
//        $('#ifSens').toggle($('select#IDsource').val()=='1');
        $('#BBH_IS').toggle($('select#bhbh_population').val()=='IS');
        $('#BBH_IIS').toggle($('select#bhbh_population').val()=='IIS');
        $('#DNS_IS').toggle($('select#nsns_population').val()=='IS');
        $('#BHNS_IS').toggle($('select#bhns_population').val()=='IS');
        $('#BHNS_IIS').toggle($('select#bhns_population').val()=='IIS');
	$('#if_with_events').toggle($('input#with_events').prop('checked'));	
        $('#give_catalogues').toggle($('input#with_events').prop('checked'));
        $('#explain_columns').toggle($('input#with_events').prop('checked'));
        $('#if_with_errors').toggle($('input#with_errors').prop('checked'));
		$('#if_grb_model').toggle($('input#grb_model').prop('checked'));
	
        checkranges();
}
updateform();
function checkranges() {
        if (!($('input#arm_length_ligo').val()>0)){
		alert("Arm Length should be larger than zero.")
                document.getElementById("arm_length_ligo").value='3995';
	}
        if (!($('input#laser_power_ligo').val()>0)){
                alert("Laser Power should be positive.");
                document.getElementById("laser_power_ligo").value='125';
        }
        if (!($('input#cavity_mirror_transmission_ligo').val()>=0) || !($('input#cavity_mirror_transmission_ligo').val()<=1)){
                alert("The cavity mirror transmission should be in between 0 and 1");
                document.getElementById("cavity_mirror_transmission_ligo").value='0.014';
        }
        if (!($('input#signal_recycling_transmission_ligo').val()>=0) || !($('input#signal_recycling_transmission_ligo').val()<=1)){
                alert("Signal recycling transmission should be in between 0 and 1");
                document.getElementById("signal_recycling_transmission_ligo").value='0.2';
        }
        if (!($('input#power_recycling_transmission_ligo').val()>=0) || !($('input#power_recycling_transmission_ligo').val()<=1)){
                alert("Power recycling transmission shoule be in between 0 and 1");
                document.getElementById("power_recycling_transmission_ligo").value='0.03';
        }
   	if (!($('input#mirror_mass_ligo').val()>0)){
                alert("The mirror mass should be positive.")
                document.getElementById("mirror_mass_ligo").value='40';
        }
	if (!($('input#signal_recycling_length_ligo').val()>0)){
                alert("The signal recycling length should be positive.");
                document.getElementById("signal_recycling_length_ligo").value='50.525';
        }
	if (!($('input#power_recycling_length_ligo').val()>0)){
                alert("The power recycling length should be positive.");
                document.getElementById("power_recycling_length_ligo").value='53';
        }
        if (!($('input#arm_length_et').val()>0)){
		alert("Arm Length should be larger than zero.");
                document.getElementById("arm_length_et").value='10000';
	}
        if (!($('input#laser_power_et').val()>0)){
                alert("Laser Power should be positive.");
                document.getElementById("laser_power_et").value='500';
        }
        if (!($('input#cavity_mirror_transmission_et').val()>0) || !($('input#cavity_mirror_transmission_et').val()<1)){
                alert("The cavity mirror transmission should be in between 0 and 1");
                document.getElementById("cavity_mirror_transmission_et").value='0.014';
        }
        if (!($('input#signal_recycling_transmission_et').val()>0) || !($('input#signal_recycling_transmission_et').val()<1)){
                alert("Signal recycling transmission should be in between 0 and 1");
                document.getElementById("signal_recycling_transmission_et").value='0.2';
        }
        if (!($('input#power_recycling_transmission_et').val()>0) || !($('input#power_recycling_transmission_et').val()<1)){
                alert("Power recycling transmission shoule be in between 0 and 1");
                document.getElementById("power_recycling_transmission_et").value='0.03';
        }
   	if (!($('input#mirror_mass_et').val()>0)){
                alert("The mirror mass should be positive.")
                document.getElementById("mirror_mass_et").value='200';
        }
	if (!($('input#signal_recycling_length_et').val()>0)){
                alert("The signal recycling length should be positive.");
                document.getElementById("signal_recycling_length_et").value='50.525';
        }
	if (!($('input#power_recycling_length_et').val()>0)){
                alert("The power recycling length should be positive.");
                document.getElementById("power_recycling_length_et").value='53';
        }
        // models
        if (!($('input#Rn_BBH_IS').val()>0)){
                alert("Rn needs to be positive.");
                document.getElementById("Rn_BBH_IS").value='13';
	}
	if (!($('input#tau_BBH_IS').val()>0.1) || !($('input#tau_BBH_IS').val()<100)){
		alert("tau needs to be in between 0.1-100");
                document.getElementById("tau_BBH_IS").value='3';
	}
	if (!($('input#mu_BBH_IS').val()>0)){
		alert("mu needs to be positive.");
                document.getElementById("mu_BBH_IS").value='3';
	}
	if (!($('input#c_BBH_IS').val()>0)){
		alert("c needs to be positive.");
		document.getElementById("c_BBH_IS").value='6';
	}	
	if (!($('input#gamma_BBH_IS').val()>1)){
		alert("gamma needs to be larger than 1, otherwise can't normalise.");
		document.getElementById("gamma_BBH_IS").value='2.5';
	}	
        if (!($('input#mcut_BBH_IS').val()>($('input#c_BBH_IS').val()/$('input#gamma_BBH_IS').val()+$('input#mu_BBH_IS').val()))){
		alert("m_cut needs to be larger than c/gamma+mu.");
                document.getElementById("mcut_BBH_IS").value='95';
	}
        if (!($('input#ql_BBH_IS').val()>0) || !($('input#ql_BBH_IS').val()<1)){
		alert("ql needs to be in between 0 and 1.");
		document.getElementById("ql_BBH_IS").value='0.4';
	}
	if (!($('input#sigx_BBH_IS').val()>0)){
		alert("sigx needs to be positive.");
		document.getElementById("sigx_BBH_IS").value='0.1';
	} 
        if (!($('input#Rn_BBH_IIS').val()>0)){
                alert("Rn needs to be positive.");
                document.getElementById("Rn_BBH_IIS").value='13';
	}
	if (!($('input#tau_BBH_IIS').val()>0.1) || !($('input#tau_BBH_IIS').val()<100)){
		alert("tau needs to be in between 0.1-100");
                document.getElementById("tau_BBH_IIS").value='3';
	}
	if (!($('input#mu_BBH_IIS').val()>0)){
		alert("mu should be positive.");
                document.getElementById("mu_BBH_IIS").value='3';
	}
	if (!($('input#c_BBH_IIS').val()>0)){
		alert("c needs to be positive.");
		document.getElementById("c_BBH_IIS").value='6';
	}	
	if (!($('input#gamma_BBH_IIS').val()>1)){
		alert("gamma should >1, otherwise can't normalise.");
		document.getElementById("gamma_BBH_IIS").value='2.5';
	}	
        if (!($('input#mcut_BBH_IIS').val()>($('input#c_BBH_IIS').val()/$('input#gamma_BBH_IIS').val()+$('input#mu_BBH_IIS').val()))){
		alert("m_cut needs to be larger than c/gamma+mu.");
                document.getElementById("mcut_BBH_IIS").value='95';
	}
        if (!($('input#ql_BBH_IIS').val()>0) || !($('input#ql_BBH_IIS').val()<1)){
		alert("ql needs to be in between 0 and 1.");
		document.getElementById("ql_BBH_IIS").value='0.4';
	}
	if (!($('input#sigx_BBH_IIS').val()>0)){
		alert("sigx needs to be positive.");
		document.getElementById("sigx_BBH_IIS").value='0.1';
	}
	if (!($('input#mpeakscale_BBH_IIS').val()>0)){
		alert("m_peak_scale needs to be positive.");
		document.getElementById("mpeakscale_BBH_IIS").value='0.002';	    }
	if (!($('input#mpeak_BBH_IIS').val()>0)){
		alert("m_peak needs to be positive.");
		document.getElementById("mpeak_BBH_IIS").value='40';		   }
	if (!($('input#mpeaksig_BBH_IIS').val()>0)){ 
		alert("m_peak_sig needs to be positive.");
		document.getElementById("mpeaksig_BBH_IIS").value='1';	           } 
        // models
        if (!($('input#Rn_DNS_IS').val()>0)){
                alert("Rn needs to be positive.");
                document.getElementById("Rn_DNS_IS").value='300';
	}
	if (!($('input#tau_DNS_IS').val()>0.1) || !($('input#tau_DNS_IS').val()<100)){
		alert("tau needs to be in between 0.1-100");
                document.getElementById("tau_DNS_IS").value='3';
	}
        if (!($('input#mlow_DNS_IS').val()>0)){
       		alert("mlow needs to be positive");
		document.getElementById("mlow_DNS_IS").value='1.1';
	}
        if (!($('input#mhigh_DNS_IS').val()>$('input#mlow_DNS_IS').val())){
       		alert("mhigh needs to be larger than mlow");
		document.getElementById("mhigh_DNS_IS").value='2.5';
	}

        if (!($('input#mmean_DNS_IS').val()>=$('input#mlow_DNS_IS').val())||!($('input#mmean_DNS_IS').val()<=$('input#mhigh_DNS_IS').val())){
		alert("mmean needs to be in between mlow and mhigh");
		num=0.5*(Number($('input#mlow_DNS_IS').val())+Number($('input#mhigh_DNS_IS').val()))
                document.getElementById("mmean_DNS_IS").value=num.toString(10)
	}
        if (!($('input#mscale_DNS_IS').val()>=0)){
		alert("mscale needs to be larger than 0.")
		document.getElementById("mscale_DNS_IS").value='0.5'
	}
	if (!($('input#sigx_DNS_IS').val()>0)){
		alert("sigx needs to be positive.");
		document.getElementById("sigx_DNS_IS").value='0.05';
	}
        if (!($('input#Rn_BHNS_IS').val()>0)){
                alert("Rn needs to be positive.");
                document.getElementById("Rn_BHNS_IS").value='45';
	}
	if (!($('input#tau_BHNS_IS').val()>0.1) || !($('input#tau_BHNS_IS').val()<100)){
		alert("tau needs to be in between 0.1-100");
                document.getElementById("tau_BHNS_IS").value='3';
	}
	if (!($('input#mu_BHNS_IS').val()>0)){
		alert("mu needs to be positive");
                document.getElementById("mu_BHNS_IS").value='3';
	}
	if (!($('input#c_BHNS_IS').val()>0)){
		alert("c needs to be positive.");
		document.getElementById("c_BHNS_IS").value='15';
	}	
	if (!($('input#gamma_BHNS_IS').val()>1)){
		alert("gamma should >1, otherwise can't normalise.");
		document.getElementById("gamma_BHNS_IS").value='2.5';
	}	
        if (!($('input#mcut_BHNS_IS').val()>($('input#c_BHNS_IS').val()/$('input#gamma_BHNS_IS').val()+$('input#mu_BHNS_IS').val()))){
		alert("m_cut needs to be larger than c/gamma+mu.");
                document.getElementById("mcut_BHNS_IS").value='95';
	}
	if (!($('input#sigx_BHNS_IS').val()>0)){
		alert("sigx needs to be positive.");
		document.getElementById("sigx_BHNS_IS").value='0.1';
	} 
        if (!($('input#mlow_BHNS_IS').val()>0)){
       		alert("mlow needs to be positive");
		document.getElementById("mlow_BHNS_IS").value='1.1';
	}
        if (!($('input#mhigh_BHNS_IS').val()>$('input#mlow_BHNS_IS').val())){
       		alert("mhigh needs to be larger than mlow");
		document.getElementById("mhigh_BHNS_IS").value='2.5';
	}

        if (!($('input#mmean_BHNS_IS').val()>=$('input#mlow_BHNS_IS').val())||!($('input#mmean_BHNS_IS').val()<=$('input#mhigh_BHNS_IS').val())){
		alert("mmean needs to be in between mlow and mhigh");
		num=0.5*(Number($('input#mlow_BHNS_IS').val())+Number($('input#mhigh_BHNS_IS').val()))
                document.getElementById("mmean_BHNS_IS").value=num.toString(10)
	}
        if (!($('input#mscale_BHNS_IS').val()>=0)){
		alert("mscale needs to be larger than 0.")
		document.getElementById("mscale_BHNS_IS").value='0.5'
	}
        if (!($('input#Rn_BHNS_IIS').val()>0)){
                alert("Rn needs to be positive.");
                document.getElementById("Rn_BHNS_IIS").value='45';
	}
	if (!($('input#tau_BHNS_IIS').val()>0.1) || !($('input#tau_BHNS_IIS').val()<100)){
		alert("tau needs to be in between 0.1-100");
                document.getElementById("tau_BHNS_IIS").value='3';
	}
	if (!($('input#mu_BHNS_IIS').val()>0)){
		alert("mu needs to be positive.");
                document.getElementById("mu_BHNS_IIS").value='3';
	}
	if (!($('input#c_BHNS_IIS').val()>0)){
		alert("c needs to be positive.");
		document.getElementById("c_BHNS_IIS").value='15';
	}	
	if (!($('input#gamma_BHNS_IIS').val()>1)){
		alert("gamma should >1, otherwise can't normalise.");
		document.getElementById("gamma_BHNS_IIS").value='2.5';
	}	
        if (!($('input#mcut_BHNS_IIS').val()>($('input#c_BHNS_IIS').val()/$('input#gamma_BHNS_IIS').val()+$('input#mu_BHNS_IIS').val()))){
		alert("m_cut needs to be larger than c/gamma+mu.");
                document.getElementById("mcut_BHNS_IIS").value='95';
	}
	if (!($('input#sigx_BHNS_IIS').val()>0)){
		alert("sigx needs to be positive.");
		document.getElementById("sigx_BHNS_IIS").value='0.1';
	} 
        if (!($('input#mlow_BHNS_IIS').val()>0)){
       		alert("mlow needs to be positive");
		document.getElementById("mlow_BHNS_IIS").value='1.1';
	}
        if (!($('input#mhigh_BHNS_IIS').val()>$('input#mlow_BHNS_IIS').val())){
       		alert("mhigh needs to be larger than mlow");
		document.getElementById("mhigh_BHNS_IIS").value='2.5';
	}
	if (!($('input#mpeakscale_BHNS_IIS').val()>0)){
		alert("m_peak_scale needs to be positive.");
		document.getElementById("mpeakscale_BHNS_IIS").value='0.002';	    }
	if (!($('input#mpeak_BHNS_IIS').val()>0)){
		alert("m_peak needs to be positive.");
		document.getElementById("mpeak_BHNS_IIS").value='40';		   }
	if (!($('input#mpeaksig_BHNS_IIS').val()>0)){ 
		alert("m_peak_sig needs to be positive.");
		document.getElementById("mpeaksig_BHNS_IIS").value='1';	           } 
	//observation and cosmology
	if (!($('input#time').val()>0)){
		alert("Time must be positive.");
		document.getElementById("time").value='3650';
		}
	if (!($('input#snr').val()>=0)){
		alert("snr must be non-negative.");
		document.getElementById("snr").value='8';
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
	if (!($('input#max_events').val()<=50000 )|| !($('input#max_events').val()>0)){
		alert("We constrain the range of max_event in 0-10000. For a larger catalogue, please run the pacakge in your local.")
		document.getElementById("max_events").value='100';	
		}	
 
}


var busy = false;
function submitform() {
	// disable submit button to prevent repetitive activation
	// TODO: choose a nicer layout framework because the current one doesn't support the disabed rendering
	// TODO: handle errors encoded as a msg in the python response (i.e. expected errors)
	//alert("running submitform")
	let form = $('form#setup');
	form.prop('disabled', true);
    //window.location = (""+window.location).replace(/#[A-Za-z0-9_]*$/,'')+"#myAnchor"  
    jump("status")
    $('#status').html("<img src='/images/Ellipsis-1.4s-50px.gif' />");
	// submit data
        // clear potential old results
        $('#total').empty()
		$('#total_true').empty()
		$('#tot_all').empty()///////////////////////////////////////
        // $('#sensitivity.plot').empty()
        $('#plot.plot').empty()
        $('#table').empty()
		$('#table2').empty();////////////////////////
        //working on new results
	const data = form.serialize();
	const url = form.attr('action');
	$.post(url, data)
		.done(function(data) {
			// when done, process data
			console.log(data);

			if (!data.success) {
                $('#status').html("Waiting for your input ...");
				alert("Request successful but server replied with an error: "+data.msg);
				return;
			}
			$('#total').text(data['total'].toPrecision(3));
			$('#total_true').text(data['total_true'].toPrecision(3));
			$('#tot_all').text(data['tot_all'].toPrecision(3));////////////////////////////////////////////
			
			// make_sensitivity_plot(data);
			make_vs_plot(data);
            plot_options_changed()
			make_table(data.events,'table');
			make_table(data.eventall,'table2');////////////////////////////
            $('#status').html(" ");
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
		name: data['config']['detector_type']
	};
	let plotdata = [trace];
	
	
	// prepare a trace for the default comparable detector
	// TODO; untested because this part of the server code doesn't work
	if (data['config']['detector_type'].endsWith('-like')) {
		let default_trace = {
			x: data['default_sensitivity'][0],
			y: data['default_sensitivity'][1],
			mode: 'line',
			name: data['config']['detector_type'].slice(0, -5)
		}
		plotdata.push(default_trace);
	}

	// define a layout
	let layout = {
		title: "Sensitivity curve",
		xaxis: {
			type: 'log',
			autorange: true,
            title:"Frequency (Hz)",
            exponentformat:"power"
		},
		yaxis: {
			type: 'log',
			autorange: true,
            title: "strain (√(1/Hz))",
            exponentformat:"power"
		}
	};

	// Create or update the plot in the html
	Plotly.newPlot($('#sensitivity.plot').get(0), plotdata, layout);
    $('#downloadsenscurve').toggle(true)
}

function make_vs_plot(data) {
	form = $('form#plot_options');

	// extra the available quantities from the data
	let variables = [];
	if (data['events'] && data['events'].length > 0) {
		// quite arbitrarily take the keys from the first one
		variables = Object.keys(data['events'][0]).filter(v => v !== 'detected');
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

//function plot_options_changed() {
//	console.log('plot options changed');
//	form = $('form#plot_options');
//	let xvar = form.find('#xvar').val();
//	let yvar = form.find('#yvar').val();
//
//	let xerror = form.find('#xerror').val();
//	let yerror = form.find('#yerror').val();
//	
//	if (xvar == yvar) {
//		// TODO: better message
//		console.log('Cannot plot same variable vs itself');
//		return;
//	}
//
//	// extract series
//	let xdata = []
//	let ydata = []
//	let xerrordata = []
//	let yerrordata = []
//	for (i in window.data.events) {
//		xdata.push(window.data.events[i][xvar]);
//		ydata.push(window.data.events[i][yvar]);
//		if (xerror != 'none') xerrordata.push(window.data.events[i][xerror]);
//		if (yerror != 'none') yerrordata.push(window.data.events[i][yerror]);
//	}
//	
//	// prep data for plot
//	let trace = {
//		type: 'scattergl',
//		x: xdata,
//		y: ydata,
//		mode: 'markers'
//	};
//	// add error bars
//	if (xerror != 'none') {
//		trace['error_x'] = {
//			type: 'data',
//			array: xerrordata,
//			visible: true
//		}
//	}
//	if (yerror != 'none') {
//		trace['error_y'] = {
//			type: 'data',
//			array: yerrordata,
//			visible: true
//		}
//	}
//	
//	let plotdata = [trace];
//
//	// define a layout
//	let layout = {
//		title: xvar + " vs. " + yvar,
//		xaxis: {
//			type: form.find('#xlog').prop('checked') ? 'log' : 'linear',
//			autorange: true,
//			title: xvar
//		},
//		yaxis: {
//			type: form.find('#ylog').prop('checked') ? 'log' : 'linear',
//			autorange: true,
//			title: yvar
//		}
//	};
//
//	// Create or update the plot in the html
//	Plotly.newPlot($('#plot.plot').get(0), plotdata, layout);
//}

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
	


	// extract series
    let plotdata=[]
    let layout={}
	let xdata = []
	let ydata = []
	let xerrordata = []
	let yerrordata = []
	// table2
	let xdata2 = []
	let ydata2 = []
	let xerrordata2 = []
	let yerrordata2 = []

    if (xvar!=yvar){
        for (i in window.data.events) {
            xdata.push(window.data.events[i][xvar]);
            ydata.push(window.data.events[i][yvar]);
            if (xerror != 'none') xerrordata.push(window.data.events[i][xerror]);
            if (yerror != 'none') yerrordata.push(window.data.events[i][yerror]);
        }
		//table2
		for (i in window.data.eventall) {
            xdata2.push(window.data.eventall[i][xvar]);
            ydata2.push(window.data.eventall[i][yvar]);
            if (xerror != 'none') xerrordata2.push(window.data.eventall[i][xerror]);
            if (yerror != 'none') yerrordata2.push(window.data.eventall[i][yerror]);
        }
	// prep data for plot
		let trace = {
			type: 'scattergl',
			// x: form.find('#xlog').prop('checked') ?  xdata.map(value => Math.log10(value)) : xdata ,
			// y: form.find('#ylog').prop('checked') ?  ydata.map(value => Math.log10(value)) : ydata ,
			x: xdata,
			y: ydata,
			mode: 'markers',
			name:'GW(table1)',
			mode: 'markers',
			marker:{color:'blue',
					// opacity:0.5
					}////////////////////////////
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
		//for table2
		let trace2 = {
			type: 'scattergl',
			x: xdata2,
			y: ydata2,
			// x: form.find('#xlog').prop('checked') ?  xdata2.map(value => Math.log10(value)) : xdata2,
			// y: form.find('#ylog').prop('checked') ?  ydata2.map(value => Math.log10(value)) : ydata2,			
			name:'GRB(table2)',
			mode: 'markers',
			marker:{color:'red',
					opacity:0.9////透明度
					}
		};
		// add error bars,table2
		if (xerror != 'none') {
			trace2['error_x'] = {
				type: 'data',
				array: xerrordata2,
				visible: true
			}
		}
		if (yerror != 'none') {
			trace2['error_y'] = {
				type: 'data',
				array: yerrordata2,
				visible: true
			}
		}
		try{
            plotdata = [trace,trace2];
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
		//for table2
		for (i in window.data.eventall) {
            if (form.find('#xlog').prop('checked')){
                xdata2.push(Math.log10(window.data.eventall[i][xvar]));
            } else {
                xdata2.push(window.data.eventall[i][xvar]);
            }
            //ydata2.push(window.data.eventall[i][yvar]);
            if (xerror != 'none') xerrordata2.push(window.data.eventall[i][xerror]);
            //if (yerror != 'none') yerrordata2.push(window.data.eventall[i][yerror]);
        }      
		let trace = {
            x: xdata,
            type: 'histogram',
			histnorm: 'probability',// 归一化直方图
            // mode: 'markers',
			name:'GW(table1)',
			marker:{color:'blue',
					opacity:0.7
					}
			// nbinsx: 10 // 调整柱子数量为10
        };
		let trace2 = {
            x: xdata2,
            type: 'histogram',
			histnorm: 'probability',
            // mode: 'markers',
			name:'GRB(table2)',
			marker:{color:'red',
					opacity:0.7
					}
			// nbinsx: 10 // 调整柱子数量为10
        };
        try{
            plotdata = [trace,trace2];
        } catch(err){
        alert(err.message)
        }
		//let plotdata = [trace];
		layout = {
            autosize: false,
            width: 550,
            height: 350,
            title: form.find('#xlog').prop('checked') ? 'log '+xvar+" histrogram" : xvar + " histogram",
			barmode: 'overlay',/////////////////////////////////// 
            xaxis: {
                //type: form.find('#xlog').prop('checked') ? 'log' : 'linear',
                type: 'linear', 
                exponentformat:"power",
                autorange: true,
                title: form.find('#xlog').prop('checked') ? 'log '+xvar : xvar
            }, 
            yaxis: {
				type: form.find('#ylog').prop('checked') ? 'log' : 'linear',
                exponentformat:"power",
				autorange: true,
				title: 'Relative probability'
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


let isDownloadTabVisible = false;
function make_table(data,tableid) {
	// clear potential old table
	$('#'+tableid).empty();

	// early abort if there are 0 rows
	if (data.length == 0) {
		return;
	}

	// create the table in memory
	let table = $('<table>');
	// build header row:
	let header = $('<tr>').addClass('sticky-header');
	for (let v in data[0]) {
		let th = $('<th>');
		th.text(v);
		header.append(th);
	}
	table.append(header);
	// build data rows:
	for (let row of data) {
		let tr = $('<tr>');
		for (let v in row) {
			let td = $('<td>');
			let val = row[v];
			
			if (val === 'NaN'|| val === '-') {
				val = (val == 'NaN') ? 'NaN' : '-';
				// val = 'NaN'; // Convert 'NaN' string to string "NaN"
			} else {

			if (v === 'detected') {
				val = val ? 'true' : 'false';
				if (val === 'true') {
					td.addClass('bool-value true');
				  }
			  } else if (val == null || val == undefined) {
				val = '-';
			  } else if (['z','D(Mpc)','χ','dz','dD','dchi'].includes(v)){
				val = val.toPrecision(2);
			  } else {
				val = val.toPrecision(3);
			  }
			  if (val < 0.01 || val >= 100) {
				val = Number.parseFloat(val).toExponential();
			  }
			}
			td.text(val);
            // if (['z','D(Mpc)','χ','dz','dD','dchi'].includes(v)){
            //     rounded = val.toPrecision(2);
            //     } else {
            //     rounded = val.toPrecision(3);
            //     }
			// if (val < 0.01 || val >= 100) {
			// 	rounded = Number.parseFloat(rounded).toExponential();
			// }
			// td.text(rounded);
			tr.append(td);
		}
		table.append(tr);
	}
	// put table in dom
        // $('#downloadtab').toggle()

	// toggle download tab visibility
	  if (!isDownloadTabVisible) {
		$('#downloadtab').toggle();
		isDownloadTabVisible = true;
	  }
	 // set table width to auto
	 table.css('width', 'auto');
	$('#'+tableid).append(table);
	//$('#downloadtab').toggle()
}

  
function savetable(tableid){
    //alert("saving! round:2")
    //form = $('form#savetab');
    try {
		if(tableid === 'table1'){
        	jsondata=window.data.events
		} else {
			jsondata=window.data.eventall
		}
		// jsondata=[window.data.events,window.data.eventall] ///////////////////////////////////
        //jsondata=[]
        var file =new Blob([JSON.stringify(jsondata)], {type: 'text/plain'});
        var url = window.URL.createObjectURL(file);
        var a = document.createElement('a');
        //a.style.display = 'none';
        a.href = url;
        // the filename you want
        //a.download = form.find('#filename').val();
		if(tableid === 'table1'){
        	a.download = $('input#filename').val()+".json"
		} else {
			a.download = $('input#filename2').val()+".json"
		}
        // a.download = $('input#filename').val()+".json"
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
        jsondata={"frequency":data[0],"strain":data[1]}
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



function plot_z_distr() {
	// 设置 y 轴和 x 轴的范围和刻度类型
	plt.ylim([0.1, 200]);
	plt.xscale('log');
	plt.yscale('log');
	plt.xlabel('$z$', fontsize=14);
	plt.ylabel('Numbers', fontsize=14);
  
	// 计算直方图并设置边缘值
	const histo = [], zedge_more = [];
	const logspaceBins = Array.from({ length: 10 }, (_, i) => Math.pow(10, -2 + i * 0.07));
	joint_data[0].forEach((val) => {
	  for (let i = 0; i < logspaceBins.length - 1; i++) {
		if (val >= logspaceBins[i] && val < logspaceBins[i + 1]) {
		  histo[i] = (histo[i] || 0) + 1;
		  break;
		}
	  }
	});
	for (let i = 0; i < logspaceBins.length - 1; i++) {
	  zedge_more.push(logspaceBins[i], 0.5 * (logspaceBins[i] + logspaceBins[i + 1]));
	}
	zedge_more.push(logspaceBins[logspaceBins.length - 1]);
  
	// 计算全部数据的直方图并设置边缘值
	const histo_all = [], zedge_all_more = [];
	const logspaceAllBins = Array.from({ length: 10 }, (_, i) => Math.pow(10, -2 + i * 0.11));
	joint_data[1].forEach((val) => {
	  for (let i = 0; i < logspaceAllBins.length - 1; i++) {
		if (val >= logspaceAllBins[i] && val < logspaceAllBins[i + 1]) {
		  histo_all[i] = (histo_all[i] || 0) + 1;
		  break;
		}
	  }
	});
	for (let i = 0; i < logspaceAllBins.length - 1; i++) {
	  zedge_all_more.push(logspaceAllBins[i], 0.5 * (logspaceAllBins[i] + logspaceAllBins[i + 1]));
	}
	zedge_all_more.push(logspaceAllBins[logspaceAllBins.length - 1]);
  
	// 根据计算出的直方图和边缘值画图
	const zedge = zedge_more.slice(1, zedge_more.length - 1);
	const zedge_all = zedge_all_more.slice(1, zedge_all_more.length - 1);
	plt.step(zedge, histo, { lw: 3, label: "sGRB-Fermi/GBM", where: 'mid' });
	plt.step(zedge_all, histo_all.map((val) => val / 50), { lw: 3, label: "GW-et", where: 'mid' });
  
	plt.tight_layout();
	plt.legend({ loc: 'upper left', fontsize: 14 });
  }
  