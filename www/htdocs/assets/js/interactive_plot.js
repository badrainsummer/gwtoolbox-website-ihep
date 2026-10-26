function updateform() {
        // first collapse/uncollapse
        alert("I'm trying to pop_list")
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
}

updateform();
var busy = false;
function submitform() {
	// disable submit button to prevent repetitive activation
	// TODO: choose a nicer layout framework because the current one doesn't support the disabed rendering
	// TODO: handle errors encoded as a msg in the python response (i.e. expected errors)
	alert("running submitform")
	let form = $('form#setup');
	form.prop('disabled', true);
    $('#status').html("<img src='/images/Ellipsis-1.4s-50px.gif' />");
	// submit data
	const data = form.serialize();
	const url = form.attr('action');
	$.post(url, data)
		.done(function(data) {
			// when done, process data
			console.log(data);

			if (!data.success) {
				alert("Request successful but server replied with an error: "+data.msg);
				return;
			}

			$('#total').text(data['total']);
			make_sensitivity_plot(data);
			make_vs_plot(data);
			make_table(data);
		})
		.fail(function() {
			// TODO: build nicer error into html
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
			autorange: true
		},
		yaxis: {
			type: 'log',
			autorange: true
		}
	};

	// Create or update the plot in the html
	Plotly.newPlot($('#sensitivity.plot').get(0), plotdata, layout);
}

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
		form.find('#xerror').append(new_option.clone());
		form.find('#yerror').append(new_option.clone());
	}
	
	// save data for later
	window.data = data;
}

function plot_options_changed() {
	console.log('plot options changed');
	form = $('form#plot_options');
	let xvar = form.find('#xvar').val();
	let yvar = form.find('#yvar').val();

	let xerror = form.find('#xerror').val();
	let yerror = form.find('#yerror').val();
	
	if (xvar == yvar) {
		// TODO: better message
		console.log('Cannot plot same variable vs itself');
		return;
	}

	// extract series
	let xdata = []
	let ydata = []
	let xerrordata = []
	let yerrordata = []
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
	
	let plotdata = [trace];

	// define a layout
	let layout = {
		title: xvar + " vs. " + yvar,
		xaxis: {
			type: form.find('#xlog').prop('checked') ? 'log' : 'linear',
			autorange: true,
			title: xvar
		},
		yaxis: {
			type: form.find('#ylog').prop('checked') ? 'log' : 'linear',
			autorange: true,
			title: yvar
		}
	};

	// Create or update the plot in the html
	Plotly.newPlot($('#plot.plot').get(0), plotdata, layout);
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
			let rounded = val.toPrecision(4);
			if (val < 0.01 || val >= 100) {
				rounded = Number.parseFloat(rounded).toExponential();
			}
			td.text(rounded);
			tr.append(td);
		}
		table.append(tr);
	}
	// put table in dom
	$('#table').append(table);
	
}
