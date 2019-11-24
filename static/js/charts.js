
$(document).ready(function () {
    let chart_data = JSON.parse($("#chart").val());
    let series = [];
    let data_chart = [];

    $.each(chart_data,function(key,value){
        let shop = key;

        let param = [];
        last_val = 0;
        value.forEach(function (key,value){
            let val = {
                x: new Date(Object.keys(key)[0]),
                y: key[Object.keys(key)[0]]
            };
            param.push(val);
            last_val = key[Object.keys(key)[0]]
        });
        let val = {
                x: new Date(Date.now()),
                y: last_val
            };
        param.push(val);

        let subseries = {
            name:  shop,
            data: param
        };
        series.push(subseries);
    });

    console.log(series);

    let datasets = [];
    series.forEach(function(obj){
        let data_label=obj.name;
        let data_chart = obj.data;
        let letters_len = (data_label.toString().length);

        let border_color = 'rgba('+ (Math.random()*letters_len*35) + ', '+ (Math.random()*letters_len*30) + ', '+ (Math.random()*letters_len*30) + ', 1)';
        let background_color = 'rgba(0, 0, 0, 0)';
        if (data_label === "SigaretNet"){
            background_color = 'rgba(255, 0, 0, 0.1)'
        } else {
            background_color = 'rgba(0, 0, 0, 0)'
        };

        let dataset = {
            label: data_label,
            data: data_chart,
            borderWidth: 3,
            backgroundColor: background_color,
            borderColor: border_color,


        };
        datasets.push(dataset);
    });

    var ctx = document.getElementById('myChart');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: datasets
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: false
                    }
                }],
                xAxes:[
                    {
                        type: 'time',
                        time: {
                            unit: 'month'
                        },
                        bounds: 'ticks'
                    }
                ]
            }
        }
    });
});
