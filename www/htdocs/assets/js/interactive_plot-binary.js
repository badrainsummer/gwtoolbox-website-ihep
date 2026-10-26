function updateform() {
    
}
updateform();

var busy = false;
function submitform() {
	let form = $('form#setup');
	form.prop('disabled', true);
    jump("status")
    $('#status').html("<img src='/images/Ellipsis-1.4s-50px.gif' />");
	
    $('#period').empty()
    $('#pdis').empty()
    $('#adis').empty()
    $('#sconj').empty()
    $('#iconj').empty()
    $('#plotrv').empty()
    $('#plotbs').empty()

    form.find('input').each(function() {
        if ($(this).val() === '') {
            $(this).val($(this).attr('placeholder'));
        }
    });

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

            window.data = data;

            $('#period').text(data['period'].toPrecision(4));
            $('#pdis').text(data['pdis'].toPrecision(3));
            $('#adis').text(data['adis'].toPrecision(3));
            $('#sconj').text(data['sconj'].toPrecision(4));
            $('#iconj').text(data['iconj'].toPrecision(4));
            make_rv_plot(data);
            make_bs_plot(data);
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

function make_rv_plot(data) {
    const div = document.getElementById('plotrv');
    if (!div) return;
    div.innerHTML = '';

    const Radial_Velocity = data.Radial_Velocity;
    const phaseSlider = document.getElementById('phaseSlider');
    const phaseValue = document.getElementById('phaseValue');
    const phaseControl = document.getElementById('phase-control');

    // 初次绘图
    const trace1 = {
        x: Radial_Velocity.phase,
        y: Radial_Velocity.velocity_primary,
        mode: 'lines',
        name: 'Primary Velocity',
        line: { width: 3 }
    };
    const trace2 = {
        x: Radial_Velocity.phase,
        y: Radial_Velocity.velocity_secondary,
        mode: 'lines',
        name: 'Secondary Velocity',
        line: { width: 3 }
    };

    const layout = {
        title: 'Radial Velocity Curve',
        xaxis: { title: 'Phas (rad)'},
        yaxis: { title: 'Radial Velocity (km/s)'},
        legend: { orientation: 'h', y: -0.25 },
        margin: { t: 50, r: 20, b: 50, l: 60 },
        width: 600,
        height: 500
    };

    Plotly.newPlot(div, [trace1, trace2], layout);

    // 显示滑轴（只有在画完图后才显示）
    phaseControl.style.display = 'block';
    $('#downloadrv').toggle(true)

    // 滑轴事件
    phaseSlider.addEventListener('input', () => {
        const shift = parseFloat(phaseSlider.value);
        const shift_phase = shift * 180 / 300;
        phaseValue.textContent = shift_phase.toFixed(1);

        const shifted_primary = Radial_Velocity.velocity_primary.slice(shift).concat(Radial_Velocity.velocity_primary.slice(0, shift));
        const shifted_secondary = Radial_Velocity.velocity_secondary.slice(shift).concat(Radial_Velocity.velocity_secondary.slice(0, shift));

        // 使用 Plotly.react() 平滑更新
        const newTrace1 = {
            x: Radial_Velocity.phase,
            y: shifted_primary,
            mode: 'lines',
            name: 'Primary Velocity',
            line: { width: 3 }
        };
        const newTrace2 = {
            x: Radial_Velocity.phase,
            y: shifted_secondary,
            mode: 'lines',
            name: 'Secondary Velocity',
            line: { width: 3 }
        };

        Plotly.react(div, [newTrace1, newTrace2], layout);
    });
}

function make_bs_plot(data) {
    const div = document.getElementById('plotbs');
    if (!div) return;
    div.innerHTML = '';

    const Separation = data.Separation;
    const period = data.period;
    const timeSlider = document.getElementById('timeSlider');
    const timeValue = document.getElementById('timeValue');
    const timeControl = document.getElementById('time-control');

    // 初次绘图    
    const trace = {
        x: Separation.time,
        y: Separation.separation,
        mode: 'lines',
        line: { width: 3 }
    };

    const layout = {
        title: 'Binary Separation Curve',
        xaxis: { title: 'Time (d)'},
        yaxis: { title: 'Binary Separation (AU)'},
        legend: { orientation: 'h', y: -0.25 },
        margin: { t: 50, r: 20, b: 50, l: 60 },
        width: 600,
        height: 500
    };

    Plotly.newPlot(div, [trace], layout);

    // 显示滑轴（只有在画完图后才显示）
    timeControl.style.display = 'block';
    $('#downloadbs').toggle(true)

    // 滑轴事件
    timeSlider.addEventListener('input', () => {
        const shift = parseFloat(timeSlider.value);
        const shift_time = shift * period / 600;
        timeValue.textContent = shift_time.toFixed(1);

        const shifted_separation = Separation.separation.slice(shift).concat(Separation.separation.slice(0, shift));

        // 使用 Plotly.react() 平滑更新
        const newTrace = {
            x: Separation.time,
            y: shifted_separation,
            mode: 'lines',
            line: { width: 3 }
        };

        Plotly.react(div, [newTrace], layout);
    });
}

function savecurve_rv(){
    try {
        jsondata=window.data.Radial_Velocity
        var file =new Blob([JSON.stringify(jsondata)], {type: 'text/plain'});
        var url = window.URL.createObjectURL(file);
        var a = document.createElement('a');
        a.href = url;
        a.download = $('input#filename').val()+".json"
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    } catch (err) {
        alert(err.message)
    }
}

function savecurve_bs(){
    try {
        jsondata=window.data.Separation
        var file =new Blob([JSON.stringify(jsondata)], {type: 'text/plain'});
        var url = window.URL.createObjectURL(file);
        var a = document.createElement('a');
        a.href = url;
        a.download = $('input#filename').val()+".json"
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    } catch (err) {
        alert(err.message)
    }
}

function jump(h){
    var top = document.getElementById(h).offsetTop;
    window.scrollTo(0, top);
}
