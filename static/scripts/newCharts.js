$(document).ready(() => $('.carousel').carousel());

function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}

const CHART_COLORS = {
    red: 'rgb(255, 99, 132)',
    orange: 'rgb(255, 159, 64)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)'
};

let charts = []
let ctxs = []

function update_charts(data) {
    let carousel = $('.carousel-inner');
    carousel.empty()
    let itemInd = 0;
    for (let i = 0; i < data.length; ++i) {
        let chart = data[i];
        let dataCfg = {
            labels: chart.labels,
            datasets: []
        }
        let show_legend = true;
        for (let dataset of chart.chart) {
            dataCfg.datasets.push({
                label: dataset.line_label,
                data: dataset.data,
                borderWidth: 1,
                backgroundColor: dataset.color.map((el) => CHART_COLORS[el])
            });
            if (dataset.line_label === '') {
                show_legend = false;
            }
            if (chart.type === 'pie' || chart.type === 'doughnut') {
                let randomColours = [];
                for (let j = 0; j < dataset.data.length; ++j) {
                    randomColours.push('rgb(' + getRandomInt(256) + ', ' + getRandomInt(256) + ',' + getRandomInt(256) + ')');
                }
                dataCfg.datasets.at(-1).backgroundColor = randomColours;
                console.log(randomColours)
            }
        }
        let title = chart.title;
        let item =
            "           <div class=\"col col-md-5\">\n" +
            "               <canvas id=\"chart" + i + "\"></canvas>\n" +
            "           </div>\n"
        if (!chart.concat || i === 0) {
            item = "<div class=\"carousel-item" + (i === 0 ? " active item-ind" : " item-ind") + itemInd++ + "\">\n" +
                "<div class=\"row justify-content-md-center\">" + item + "</div></div>\n";
            carousel.append(item);
        } else {
            carousel.children().children().last().append(item);
        }

        ctxs.push(document.getElementById('chart' + i))
        console.log()
        charts.push(new Chart(ctxs.at(-1), {
            type: chart.type,
            data: dataCfg,
            options: {
                title: {
                    display: true,
                    text: title,
                    fontSize: 25
                },
                legend: {
                    display: show_legend
                },
                tooltips: {
                    callbacks: {
                        label: function (tooltipItem) {
                            return tooltipItem.yLabel;
                        }
                    }
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        },
                        scaleLabel: {
                            display: true,
                            labelString: chart.yName
                        }
                    }],
                    xAxes: [{
                        display: false,
                        scaleLabel: {
                            display: true,
                            labelString: chart.xName
                        }
                    }]
                }
            }
        }));

    }
}
