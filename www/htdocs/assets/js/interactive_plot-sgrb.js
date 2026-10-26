function updateform() {
    const selected = document.querySelector('input[name="output_type"]:checked');
    const E_range = document.getElementById("E_range");
    const T_range = document.getElementById("T_range");
    const TLightcurve = document.getElementById("TLightcurve");
    const TSpectrumBlock = document.getElementById("TSpectrum");
    const OLightcurve = document.getElementById("OLightcurve");
    const OSpectrumBlock = document.getElementById("OSpectrum");
    if (!selected) return;
    if (selected.value === "light_curve") {
        E_range.style.display =  "block";
        T_range.style.display =  "none";
        TLightcurve.style.display = "block";
        TSpectrumBlock.style.display = "none";
        OLightcurve.style.display = "block";
        OSpectrumBlock.style.display = "none";
    }
    else if (selected.value === "spectrum") {
        E_range.style.display =  "none";
        T_range.style.display =  "block";
        TLightcurve.style.display = "none";
        TSpectrumBlock.style.display = "block";
        OLightcurve.style.display = "none";
        OSpectrumBlock.style.display = "block";
    }
}
updateform();

var busy = false;
function submitform() {
	let form = $('form#setup');
	form.prop('disabled', true);
    jump("status")
    $('#status').html("<img src='/images/Ellipsis-1.4s-50px.gif' />");
	
    $('#plotTLightcurve').empty()
    $('#plotOLightcurve').empty()
    $('#plotTSpectrum').empty()
    $('#plotOSpectrum').empty()
    $('#toggleYSCALE').toggle(false)

    form.find('input').each(function() {
        if ($(this).val() === '') {
            $(this).val($(this).attr('placeholder'));
        }
    });

	const data = form.serialize();
	const url = form.attr('action');
    const selected = document.querySelector('input[name="output_type"]:checked');
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

            $('#status').html(" ");
            if (selected.value === "light_curve") {
                make_TLightcurve_plot(data);
                make_OLightcurve_plot(data);
            }
            else if (selected.value === "spectrum") {
                make_TSpectrum_plot(data);
                make_OSpectrum_plot(data);
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

let OSpectrumYAxisType = 'linear';

function make_TLightcurve_plot(data) {
    // 清空旧图像
    const div = document.getElementById('plotTLightcurve');
    if (!div) return;
    div.innerHTML = '';

    const traces = [];

    // 总谱
    const lightcurve = data.lightcurve;
    traces.push({
        x: lightcurve.T_array,
        y: lightcurve.lightcurve,
        mode: 'lines',
        line: { width: 3 }
    });

    const layout = {
        title: 'Theoretical Light Curve',
        xaxis: { title: 'Time (s)'},
        yaxis: { title: {
                     text: 'Flux (keV cm<sup>-2</sup> s<sup>-1</sup>)',
                     standoff: 10
                 }, 
                 tickformat: ".1e",
                 exponentformat: "e",
                 showexponent: "all",
                 separatethousands: false,
                 automargin: true 
        },
        legend: { orientation: 'h', y: -0.25 },
        margin: { t: 50, r: 20, b: 50, l: 60 },
        width: 600,
        height: 500
    };

    Plotly.newPlot(div, traces, layout, { responsive: true });
    $('#downloadTLightcurve').toggle(true)
}

function make_OLightcurve_plot(data) {
    const div = document.getElementById('plotOLightcurve');
    if (!div) return;
    div.innerHTML = '';

    const traces = [];

    for (const telescope in data.telescope) {
        const spec = data.telescope[telescope];
        traces.push({
            x: spec.time,
            y: spec.counts,
            error_y: {
                type: 'data',
                array: spec.uncentainty,
                visible: true
            },
            mode: 'markers',
            name: telescope,
            marker: { size: 6 }
        });
    }

    const layout = {
        title: 'Observed Light Curve',
        xaxis: { title: 'Time (s)' },
        yaxis: { title: 'Counts', type: OSpectrumYAxisType },
        legend: { orientation: 'h', y: -0.25 },
        margin: { t: 50, r: 20, b: 50, l: 60 },
        width: 600,
        height: 500
    };

    Plotly.newPlot(div, traces, layout, { responsive: true });
    $('#downloadOLightcurve').toggle(true)
    $('#toggleYSCALE').toggle(true)
}

function make_TSpectrum_plot(data) {
    // 清空旧图像
    const div = document.getElementById('plotTSpectrum');
    if (!div) return;
    div.innerHTML = '';

    const traces = [];

    // 总谱
    const spectrum = data.spectrum;
    traces.push({
        x: spectrum.E_array,
        y: spectrum.spectrum,
        mode: 'lines',
        line: { width: 3 }
    });

    const layout = {
        title: 'Theoretical Spectrum',
        xaxis: { title: 'Energy (keV)', type: 'log' },
        yaxis: { title: {
                     text: 'Flux (keV cm<sup>-2</sup> s<sup>-1</sup> keV<sup>-1</sup>)',
                     standoff: 10
                 }, 
                 type: 'log', 
                 tickformat: ".1e",
                 exponentformat: "e",
                 showexponent: "all",
                 separatethousands: false,
                 automargin: true  },
        legend: { orientation: 'h', y: -0.25 },
        margin: { t: 50, r: 20, b: 50, l: 60 },
        width: 600,
        height: 500
    };

    Plotly.newPlot(div, traces, layout, { responsive: true });
    $('#downloadTSpectrum').toggle(true)
}

function make_OSpectrum_plot(data) {
    const div = document.getElementById('plotOSpectrum');
    if (!div) return;
    div.innerHTML = '';

    const traces = [];

    for (const telescope in data.telescope) {
        const spec = data.telescope[telescope];
        traces.push({
            x: spec.energies,
            y: spec.spectrum,
            error_y: {
                type: 'data',
                array: spec.uncentainty,
                visible: true
            },
            mode: 'markers',
            name: telescope,
            marker: { size: 6 }
        });
    }

    const layout = {
        title: 'Observed Spectrum',
        xaxis: { title: 'Energy (keV)', type: 'log' },
        yaxis: { title: 'Counts', type: OSpectrumYAxisType },
        legend: { orientation: 'h', y: -0.25 },
        margin: { t: 50, r: 20, b: 50, l: 60 },
        width: 600,
        height: 500
    };

    Plotly.newPlot(div, traces, layout, { responsive: true });
    $('#downloadOSpectrum').toggle(true)
    $('#toggleYSCALE').toggle(true)
}

document.getElementById('toggleYSCALE').onclick = function () {
    OSpectrumYAxisType = (OSpectrumYAxisType === 'linear') ? 'log' : 'linear';

    const div1 = document.getElementById('plotOSpectrum');
    const div2 = document.getElementById('plotOLightcurve');

    if (div1 && div1.data) {
        Plotly.relayout(div1, { 'yaxis.type': OSpectrumYAxisType });
    }

    if (div2 && div2.data) {
        Plotly.relayout(div2, { 'yaxis.type': OSpectrumYAxisType });
    }

};

function savecurve_TLightcurve(){
    try {
        jsondata=window.data.lightcurve
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

function savecurve_OLightcurve(){
    try {
        jsondata=window.data.telescope
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

function savecurve_TSpectrum(){
    try {
        jsondata=window.data.spectrum
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

function savecurve_OSpectrum(){
    try {
        jsondata=window.data.telescope
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