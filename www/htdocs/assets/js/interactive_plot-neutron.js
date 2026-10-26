function updateform() {
    const disc = document.getElementById("disc");
    const surface = document.getElementById("surface");
    const disc_param = document.getElementById("disc_param");
    const surface_param = document.getElementById("surface_param");
    if (disc && disc_param) {
        disc_param.style.display = disc.checked ? "block" : "none";
    }
    if (surface && surface_param) {
        surface_param.style.display = surface.checked ? "block" : "none";
    }
}
updateform();

function updatetype() {
    const typeKind = document.querySelector('input[name="type_kind"]:checked').value;
    document.getElementById('LMXB_type').classList.add('hidden');
    document.getElementById('AF-AXP_type').classList.add('hidden');
    if (typeKind === 'LMXB') {
        document.getElementById('LMXB_type').classList.remove('hidden');
    } else if (typeKind === 'AF-AXP') {
        document.getElementById('AF-AXP_type').classList.remove('hidden');
    }
}
updatetype();

var busy = false;
function getparameters() {
    jump("status_typical")
    $('#status_typical').html("<img src='/images/Ellipsis-1.4s-50px.gif' />");

    let form = $('form#gettype_param');
	form.prop('disabled', true);
    const data = form.serialize();
	const url = form.attr('action');

    $('#plotTSpectrum').empty()
    $('#plotOSpectrum').empty()
    $('#plotts').empty()
    $('#plotos').empty()
    $('#toggleYSCALE').toggle(false)

    const alert_LMXB = document.getElementById("alert_LMXB");
    const alert_AMSP = document.getElementById("alert_AMSP");
    const alert_AXP_pencil = document.getElementById("alert_AXP-pencil");
    const alert_AXP_fan = document.getElementById("alert_AXP-fan");
    const alert_AXP_mix = document.getElementById("alert_AXP-mix");
    const more_ifo = document.getElementById("more_ifo");
    const disc_fields = document.getElementById("disc-fields");
    const surface_fields = document.getElementById("surface-fields");
    const sketch = document.getElementById("sketch");
    const sketch_LMXB = document.getElementById("sketch_LMXB");
    const sketch_AMSP = document.getElementById("sketch_AMSP");
    const sketch_AF_pencil = document.getElementById("sketch_AF-pencil");
    const sketch_AF_fan = document.getElementById("sketch_AF-fan");
    const sketch_AF_mix = document.getElementById("sketch_AF-mix");
    const normal_plot = document.getElementById("normal_plot");
    const AMSP_plot = document.getElementById("AMSP_plot");

    function all_none() {
        alert_LMXB.style.display = "none";
        alert_AMSP.style.display = "none";
        alert_AXP_pencil.style.display = "none";
        alert_AXP_fan.style.display = "none";
        alert_AXP_mix.style.display = "none";
        more_ifo.style.display = "none";
        disc_fields.style.display = "none";
        surface_fields.style.display = "none";
        sketch.style.display = "none";
        sketch_LMXB.style.display = "none";
        sketch_AMSP.style.display = "none";
        sketch_AF_pencil.style.display = "none";
        sketch_AF_fan.style.display = "none";
        sketch_AF_mix.style.display = "none";
        normal_plot.style.display = "none";
        AMSP_plot.style.display = "none";
    }

    all_none();

    function give_param(index, data) {
        const inputs = document.querySelectorAll("input[type='text'], input[type='number']");
        inputs.forEach(input => input.value = "");
        switch (index) {
            case 1:
                if (data.surface_theta != null) document.getElementById("surface_theta").value = Number(data.surface_theta).toPrecision(4);
                if (data.surface_iota != null) document.getElementById("surface_iota").value = Number(data.surface_iota).toPrecision(4);
            case 2:
                if (data.disc_theta != null) document.getElementById("disc_theta").value = Number(data.disc_theta).toPrecision(4);
                if (data.disc_Te != null) document.getElementById("disc_Te").value = Number(data.disc_Te).toPrecision(4);
                if (data.disc_cov_frac != null) document.getElementById("disc_cov_frac").value = Number(data.disc_cov_frac).toPrecision(4);
                if (data.disc_H != null) document.getElementById("disc_H").value = Number(data.disc_H).toPrecision(4);
                if (data.disc_Gamma != null) document.getElementById("disc_Gamma").value = Number(data.disc_Gamma).toPrecision(4);
                if (data.disc_Fe != null) document.getElementById("disc_Fe").value = Number(data.disc_Fe).toPrecision(4);
                if (data.disc_KE != null) document.getElementById("disc_KE").value = Number(data.disc_KE).toPrecision(4);
                if (data.surface_r != null) document.getElementById("surface_r").value = Number(data.surface_r).toPrecision(4);
                if (data.surface_Tbb != null) document.getElementById("surface_Tbb").value = Number(data.surface_Tbb).toPrecision(4);
                if (data.surface_Te != null) document.getElementById("surface_Te").value = Number(data.surface_Te).toPrecision(4);
                if (data.surface_cov_frac != null) document.getElementById("surface_cov_frac").value = Number(data.surface_cov_frac).toPrecision(4);
                if (data.surface_Gamma != null) document.getElementById("surface_Gamma").value = Number(data.surface_Gamma).toPrecision(4);
                if (data.surface_tau != null) document.getElementById("surface_tau").value = Number(data.surface_tau).toPrecision(4);
            case 3:
                if (data.mass != null) document.getElementById("mass").value = Number(data.mass).toPrecision(4);
                if (data.distance != null) document.getElementById("distance").value = Number(data.distance).toPrecision(4);
                document.getElementById("radius").value = 10
                if (data.B != null) document.getElementById("Bsurf").value = Number(data.B).toPrecision(4);
                if (data.period != null) document.getElementById("P").value = Number(data.period).toPrecision(4);
                if (data.mdot != null) document.getElementById("mdot").value = Number(data.mdot).toPrecision(4);
        }
    }

    $.post(url, data)
		.done(function(data) {
			// when done, process data
			console.log(data);
			if (!data.success) {
                $('#status_typical').html(" ");
				alert("Request successful but server replied with an error: "+data.msg);
				return;
			}
            $('#status_typical').html(" ");
            switch (data.config.type_kind) {
                case "LMXB":
                    alert_LMXB.style.display = "block";
                    sketch.style.display = "block";
                    sketch_LMXB.style.display = "block";
                    more_ifo.style.display = "block";
                    disc_fields.style.display = "block";
                    surface_fields.style.display = "block";
                    normal_plot.style.display = "block";
                    document.getElementById("type").value = "LMXB"
                    give_param(2, data)
                    break;
                case "AF-AMXP":
                    alert_AMSP.style.display = "block";
                    sketch.style.display = "block";
                    sketch_AMSP.style.display = "block";
                    more_ifo.style.display = "block";
                    disc_fields.style.display = "block";
                    surface_fields.style.display = "block";
                    AMSP_plot.style.display = "block";
                    document.getElementById("type").value = "AF-AMSP"
                    give_param(1, data)
                    break;
                case "AF-AXP":
                    document.getElementById("type").value = data.config.type_AF_AXP
                    switch (data.config.type_AF_AXP) {
                        case "AF-AXP-pencil":
                            alert_AXP_pencil.style.display = "block";
                            sketch.style.display = "block";
                            sketch_AF_pencil.style.display = "block";
                            more_ifo.style.display = "block";
                            normal_plot.style.display = "block";
                            break;
                        case "AF-AXP-fan":
                            alert_AXP_fan.style.display = "block";
                            sketch.style.display = "block";
                            sketch_AF_fan.style.display = "block";
                            more_ifo.style.display = "block";
                            normal_plot.style.display = "block";
                            break;
                        case "AF-AXP-mix":
                            alert_AXP_mix.style.display = "block";
                            sketch.style.display = "block";
                            sketch_AF_mix.style.display = "block";
                            more_ifo.style.display = "block";
                            normal_plot.style.display = "block";
                            break;
                    }
                    give_param(3, data)
                    break;
            }

		})
		.fail(function() {
			// TODO: build nicer error into html
            $('#status_typical').html(" ");
			alert("Oops, something went wrong!");
		})
		.always(function() {
			// always re-enable all form elements
            $('#status_typical').html(" ");
			form.prop('disabled', false);
		});

	// supress normal form handler
	return false;
}

var busy = false;
function submitcheck() {
    let form = $('form#classification_check');
	form.prop('disabled', true);
    jump("check_status")
    $('#check_status').html("<img src='/images/Ellipsis-1.4s-50px.gif' />");

    $('#plotTSpectrum').empty()
    $('#plotOSpectrum').empty()
    $('#plotts').empty()
    $('#plotos').empty()
    $('#toggleYSCALE').toggle(false)

	const data = form.serialize();
	const url = form.attr('action');

    const alert_LMXB = document.getElementById("alert_LMXB");
    const alert_AMSP = document.getElementById("alert_AMSP");
    const alert_AXP_pencil = document.getElementById("alert_AXP-pencil");
    const alert_AXP_fan = document.getElementById("alert_AXP-fan");
    const alert_AXP_mix = document.getElementById("alert_AXP-mix");
    const alert_PPL = document.getElementById("alert_PPL");
    const alert_PS = document.getElementById("alert_PS");
    const alert_bad = document.getElementById("alert_bad");
    const more_ifo = document.getElementById("more_ifo");
    const disc_fields = document.getElementById("disc-fields");
    const surface_fields = document.getElementById("surface-fields");
    const sketch = document.getElementById("sketch");
    const sketch_LMXB = document.getElementById("sketch_LMXB");
    const sketch_AMSP = document.getElementById("sketch_AMSP");
    const sketch_AF_pencil = document.getElementById("sketch_AF-pencil");
    const sketch_AF_fan = document.getElementById("sketch_AF-fan");
    const sketch_AF_mix = document.getElementById("sketch_AF-mix");
    const sketch_PPL = document.getElementById("sketch_PPL");
    const normal_plot = document.getElementById("normal_plot");
    const AMSP_plot = document.getElementById("AMSP_plot");

    function all_none() {
        alert_LMXB.style.display = "none";
        alert_AMSP.style.display = "none";
        alert_AXP_pencil.style.display = "none";
        alert_AXP_fan.style.display = "none";
        alert_AXP_mix.style.display = "none";
        alert_PPL.style.display = "none";
        alert_PS.style.display = "none";
        alert_bad.style.display = "none";
        more_ifo.style.display = "none";
        disc_fields.style.display = "none";
        surface_fields.style.display = "none";
        sketch.style.display = "none";
        sketch_LMXB.style.display = "none";
        sketch_AMSP.style.display = "none";
        sketch_AF_pencil.style.display = "none";
        sketch_AF_fan.style.display = "none";
        sketch_AF_mix.style.display = "none";
        sketch_PPL.style.display = "none";
        normal_plot.style.display = "none";
        AMSP_plot.style.display = "none";
    }

    all_none();

	$.post(url, data)
		.done(function(data) {
			// when done, process data
			console.log(data);
			if (!data.success) {
                $('#check_status').html("Waiting for your input ...");
				alert("Request successful but server replied with an error: "+data.msg);
				return;
			}

            document.getElementById("type").value = data.class
            switch (data.class) {
                case 'LMXB':
                    alert_LMXB.style.display = "block";
                    sketch.style.display = "block";
                    sketch_LMXB.style.display = "block";
                    more_ifo.style.display = "block";
                    disc_fields.style.display = "block";
                    surface_fields.style.display = "block";
                    normal_plot.style.display = "block";
                    break;
                case 'AF-AMSP':
                    alert_AMSP.style.display = "block";
                    sketch.style.display = "block";
                    sketch_AMSP.style.display = "block";
                    more_ifo.style.display = "block";
                    disc_fields.style.display = "block";
                    surface_fields.style.display = "block";
                    AMSP_plot.style.display = "block";
                    break;
                case 'AF-AXP-pencil':
                    alert_AXP_pencil.style.display = "block";
                    sketch.style.display = "block";
                    sketch_AF_pencil.style.display = "block";
                    more_ifo.style.display = "block";
                    normal_plot.style.display = "block";
                    break;
                case 'AF-AXP-fan':
                    alert_AXP_fan.style.display = "block";
                    sketch.style.display = "block";
                    sketch_AF_fan.style.display = "block";
                    more_ifo.style.display = "block";
                    normal_plot.style.display = "block";
                    break;
                case 'AF-AXP-mix':
                    alert_AXP_mix.style.display = "block";
                    sketch.style.display = "block";
                    sketch_AF_mix.style.display = "block";
                    more_ifo.style.display = "block";
                    normal_plot.style.display = "block";
                    break;
                case 'PPL':
                    alert_PPL.style.display = "block";
                    sketch.style.display = "block";
                    sketch_PPL.style.display = "block";
                    break;
                case 'PS':
                    alert_PS.style.display = "block";
                    break;
                case 'bad':
                    alert_bad.style.display = "block";
                    break;
            }
            $('#check_status').html(" ");

		})
		.fail(function() {
			// TODO: build nicer error into html
            $('#check_status').html("Waiting for your input ...");
			alert("Oops, something went wrong!");
		})
		.always(function() {
			// always re-enable all form elements
			form.prop('disabled', false);
		});

	// supress normal form handler
	return false;
}

var busy = false;
function submitform() {
    let form = $('form#setup');
	form.prop('disabled', true);
    jump("status")
    $('#status').html("<img src='/images/Ellipsis-1.4s-50px.gif' />");
	
    $('#plotTSpectrum').empty()
    $('#plotOSpectrum').empty()
    $('#plotts').empty()
    $('#plotos').empty()
    $('#toggleYSCALE').toggle(false)

    const formData = form.serializeArray();

    const extraFields = ['mass', 'distance', 'radius', 'Bsurf', 'P', 'mdot'];
    extraFields.forEach(id => {
        const el = document.getElementById(id);
        if (el && el.value.trim() !== '') {
            formData.push({ name: id, value: el.value });
        }
    });

	// const data = form.serialize();
	const url = form.attr('action');
    const data = $.param(formData);
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
            if (["LMXB", "AF-AXP-pencil", "AF-AXP-mix", "AF-AXP-fan"].includes(data['config']['type'])) {
                make_TSpectrum_plot(data);
                make_OSpectrum_plot(data);
            } else if (data['config']['type'] == "AF-AMSP") {
                make_ts_plot(data);
                make_os_plot(data)
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
        xaxis: { title: 'Energy (keV)', 
                 type: 'log'},
        yaxis: { title: {
                     text: 'Flux (keV cm<sup>-2</sup> s<sup>-1</sup> keV<sup>-1</sup>)',
                     standoff: 10
                 }, 
                 type: 'log', 
                 range: [-20, -6],
                 tickformat: ".1e",
                 exponentformat: "e",
                 showexponent: "all",
                 separatethousands: false,
                 automargin: true},
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
        yaxis: { title: 'Counts', type: OSpectrumYAxisType},
        legend: { orientation: 'h', y: -0.25 },
        margin: { t: 50, r: 20, b: 50, l: 60 },
        width: 600,
        height: 500
    };

    Plotly.newPlot(div, traces, layout, { responsive: true });
    $('#downloadOSpectrum').toggle(true)
    $('#toggleYSCALE').toggle(true)
}

function make_ts_plot(data) {
    const div = document.getElementById('plotts');
    if (!div) return;
    div.innerHTML = '';

    const traces = [];
    const total = data.TSpectrum.total;
    const phaseSlider = document.getElementById('phaseSlider_1');
    const phaseValue = document.getElementById('phaseValue_1');
    const phaseControl = document.getElementById('phase-control_1');

    // 初次绘图    
    traces.push({
        x: total.Energy[0],
        y: total.Flux[0],
        mode: 'lines',
        name: 'Total Spectrum',
        line: { width: 3 }
    });

    // 各个分量（除了 total）
    for (const key in data.TSpectrum) {
        if (key === 'total') continue;
        const comp = data.TSpectrum[key];
        traces.push({
            x: comp.Energy[0],
            y: comp.Flux[0],
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
                 range: [-20, -6],
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

    Plotly.newPlot(div, traces, layout);

    // 显示滑轴（只有在画完图后才显示）
    phaseControl.style.display = 'block';
    $('#downloadts').toggle(true)

    // 滑轴事件
    phaseSlider.addEventListener('input', () => {
        const shift = parseInt(phaseSlider.value);
        phaseValue.textContent = ((shift/9*2).toFixed(2) + "π");
        const newtraces = [];

        // 使用 Plotly.react() 平滑更新
        newtraces.push({
            x: total.Energy[shift],
            y: total.Flux[shift],
            mode: 'lines',
            name: 'Total Spectrum',
            line: { width: 3 }
        });

        // 各个分量（除了 total）
        for (const key in data.TSpectrum) {
            if (key === 'total') continue;
            const comp = data.TSpectrum[key];
            newtraces.push({
                x: comp.Energy[shift],
                y: comp.Flux[shift],
                mode: 'lines',
                name: key,
                line: { dash: 'dot' }
            });
        }

        Plotly.react(div, newtraces, layout);
    });
}

function make_os_plot(data) {
    const div = document.getElementById('plotos');
    if (!div) return;
    div.innerHTML = '';

    const traces = [];
    const phaseSlider = document.getElementById('phaseSlider_2');
    const phaseValue = document.getElementById('phaseValue_2');
    const phaseControl = document.getElementById('phase-control_2');

    // 初次绘图
    for (const telescope in data.OSpectrum) {
        const spec = data.OSpectrum[telescope];
        traces.push({
            x: spec.Energy[0],
            y: spec.Counts[0],
            error_y: {
                type: 'data',
                array: spec.uncertainties[0],
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

    Plotly.newPlot(div, traces, layout);

    // 显示滑轴（只有在画完图后才显示）
    phaseControl.style.display = 'block';
    $('#downloados').toggle(true)
    $('#toggleYSCALE').toggle(true)

    // 滑轴事件
    phaseSlider.addEventListener('input', () => {
        const shift = parseInt(phaseSlider.value);
        phaseValue.textContent = ((shift/9*2).toFixed(2) + "π");
        const newtraces = [];

        // 使用 Plotly.react() 平滑更新
        for (const telescope in data.OSpectrum) {
            const spec = data.OSpectrum[telescope];
            newtraces.push({
                x: spec.Energy[shift],
                y: spec.Counts[shift],
                error_y: {
                    type: 'data',
                    array: spec.uncertainties[shift],
                    visible: true
                },
                mode: 'markers',
                name: telescope,
                marker: { size: 6 }
            });
        }

        Plotly.react(div, newtraces, layout);
    });
}

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

document.getElementById('toggleYSCALE').onclick = function () {
    OSpectrumYAxisType = (OSpectrumYAxisType === 'linear') ? 'log' : 'linear';

    const div1 = document.getElementById('plotOSpectrum');
    const div2 = document.getElementById('plotos');

    if (div1 && div1.data) {
        Plotly.relayout(div1, { 'yaxis.type': OSpectrumYAxisType });
    }

    if (div2 && div2.data) {
        Plotly.relayout(div2, { 'yaxis.type': OSpectrumYAxisType });
    }
};

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

function savecurve_ts(){
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

function savecurve_os(){
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

function jump(h){
    var top = document.getElementById(h).offsetTop;
    window.scrollTo(0, top);
}