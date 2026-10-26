function updateform() {
    const checkbox = document.getElementById("use_corona");
    const fields = document.getElementById("corona-fields");
    const sketch = document.getElementById("sketch");
    const sketch_corona = document.getElementById("sketch_corona");
    if (checkbox && fields) {
        fields.style.display = checkbox.checked ? "block" : "none";
        sketch.style.display = checkbox.checked ? "none" : "block";
        sketch_corona.style.display = checkbox.checked ? "block" : "none";
    }

    const telescopeCheckboxes = document.querySelectorAll("#telescope input[type='checkbox']");
    const anyChecked = Array.from(telescopeCheckboxes).some(cb => cb.checked);
    const osBlock = document.getElementById("OSpectrum");
        osBlock.style.display = anyChecked ? "block" : "none";
}
updateform();

var busy = false;
function submitform() {
	let form = $('form#setup');
	form.prop('disabled', true);
    jump("status")
    $('#status').html("<img src='/images/Ellipsis-1.4s-50px.gif' />");
	
    $('#plotTSpectrum').empty()
    $('#plotOSpectrum').empty()
    $('#toggleYSCALE').toggle(false)

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

            make_TSpectrum_plot(data);
            if (data.OSpectrum) {
                make_OSpectrum_plot(data);
            }
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

let OSpectrumYAxisType = 'linear';

function make_TSpectrum_plot(data) {
    // 清空旧图像
    const div = document.getElementById('plotTSpectrum');
    if (!div) return;
    div.innerHTML = '';

    const traces = [];

    // 总谱
    const total = data.TSpectrum.total;
    traces.push({
        x: total.Energy,
        y: total.Flux,
        mode: 'lines',
        name: 'Total Spectrum',
        line: { width: 3 }
    });

    // 各个分量（除了 total）
    for (const key in data.TSpectrum) {
        if (key === 'total') continue;
        const comp = data.TSpectrum[key];
        traces.push({
            x: comp.Energy,
            y: comp.Flux,
            mode: 'lines',
            name: key,
            line: { dash: 'dot' }
        });
    }

    const layout = {
        title: 'Theoretical Spectrum',
        xaxis: { title: 'Energy (keV)', type: 'log' },
        yaxis: { title: {
                     text: 'Flux (keV cm<sup>-2</sup> s<sup>-1</sup> keV<sup>-1</sup>)',
                     standoff: 10
                 }, 
                 type: 'log', 
                 range: [-15, -8],
                 tickformat: ".1e",
                 exponentformat: "e",
                 showexponent: "all",
                 separatethousands: false,
                 automargin: true },
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

    for (const telescope in data.OSpectrum) {
        const spec = data.OSpectrum[telescope];
        traces.push({
            x: spec.Energy,
            y: spec.Counts,
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
        xaxis: { title: 'Energy (keV)' },
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

    Plotly.relayout('plotOSpectrum', {
        'yaxis.type': OSpectrumYAxisType
    });
};

function savecurve_TSpectrum(){
    try {
        jsondata=window.data.TSpectrum
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
        jsondata=window.data.OSpectrum
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

async function generateParams(type) {
    jump("status_typical");
    $('#status_typical').html("<img src='/images/Ellipsis-1.4s-50px.gif' />");
    try {
        const response = await fetch("cgi-bin/type-blackhole.py", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: `type=${encodeURIComponent(type)}`
        });
        $('#status_typical').html(" ");

        if (!response.ok) throw new Error("Network response was not ok");

        const data = await response.json();

        // 填充黑洞参数
        if (data.mass !== undefined) document.getElementById("mass").value = Number(data.mass).toPrecision(4);
        if (data.distance !== undefined) document.getElementById("distance").value = Number(data.distance).toPrecision(4);

        // 填充盘参数
        if (data.mdot !== undefined) document.getElementById("mdot").value = Number(data.mdot).toPrecision(4);
        if (data.theta !== undefined) document.getElementById("theta").value = Number(data.theta).toPrecision(4);
        if (data.rin !== undefined) document.getElementById("rin").value = Number(data.rin).toPrecision(4);

        // 填充日冕参数
        const coronaCheckbox = document.getElementById("use_corona");
        if (coronaCheckbox) {
            coronaCheckbox.checked = true;
        }
        if (data.Te !== undefined) document.getElementById("Te").value = Number(data.Te).toPrecision(4);
        if (data.cov_frac !== undefined) document.getElementById("cov_frac").value = Number(data.cov_frac).toPrecision(4);
        if (data.H !== undefined) document.getElementById("H").value = Number(data.H).toPrecision(4);
        if (data.Gamma !== undefined) document.getElementById("Gamma").value = Number(data.Gamma).toPrecision(4);
        if (data.Fe !== undefined) document.getElementById("Fe").value = Number(data.Fe).toPrecision(4);
        if (data.KE !== undefined) document.getElementById("KE").value = Number(data.KE).toPrecision(4);

        console.log("Parameters filled:", data);
    } catch (err) {
        $('#status_typical').html(" ");
        alert("Failed to generate parameters: " + err.message);
    }
}
