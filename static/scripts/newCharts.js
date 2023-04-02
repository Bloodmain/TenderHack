$(document).ready(() => $('.carousel').carousel().on('slide.bs.carousel', function () {
        adjust_suggestions()
    }
));

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


function isDonut(chart) {
    return chart.type === 'pie' || chart.type === 'doughnut';
}

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
        pieCfg = {
            hoverOffset: 40,
            hoverBorderWidth: 10,
            hoverBorderColor: CHART_COLORS.grey
        }
        for (let dataset of chart.chart) {
            dataCfg.datasets.push(Object.assign({}, {
                label: dataset.line_label,
                data: dataset.data,
                borderWidth: 1,
                backgroundColor: dataset.color.map((el) => CHART_COLORS[el]),
            }, (isDonut(chart) ? pieCfg : {})));
            if (dataset.line_label === '') {
                show_legend = false;
            }
            if (isDonut(chart)) {
                let randomColours = [];
                for (let j = 0; j < dataset.data.length; ++j) {
                    randomColours.push('rgb(' + getRandomInt(256) + ', ' + getRandomInt(256) + ',' + getRandomInt(256) + ')');
                }
                dataCfg.datasets.at(-1).backgroundColor = randomColours;
            }
        }
        let title = chart.title;
        let item =
            "           <div class=\"col col-xl-9\">\n" +
            "               <canvas id=\"chart" + i + "\"></canvas>\n" +
            "           </div>\n";

        item = "<div class=\"row justify-content-md-center charts\">" + item + "</div>"

        if (!chart.concat || i === 0) {
            item = "<div class=\"carousel-item" + (i === 0 ? " active item-ind" : " item-ind") + itemInd++ + "\">\n"
                + item + "</div>\n";
            carousel.append(item);
        } else {
            carousel.children().last().append(item);
        }

        ctxs.push(document.getElementById('chart' + i))
        charts.push(new Chart(ctxs.at(-1), {
            type: chart.type,
            radius: 5,
            data: dataCfg,
            options: {
                radius: "75%",
                plugins: {
                    zoom: {
                        pan: {
                            enabled: true,
                            mode: 'x'
                        },
                        zoom: {
                            sensitivity: 0.5,
                            wheel: {
                                enabled: true,
                            },
                            pinch: {
                                enabled: true
                            },
                            mode: 'x',
                        }
                    },
                    legend: {
                        display: show_legend
                    },
                    title: {
                        display: true,
                        text: title,
                        font: {size: 22}
                    },
                },


                tooltips: {
                    callbacks: {
                        label: function (tooltipItem) {
                            return tooltipItem.yLabel;
                        }
                    }
                },
                scales: {
                    y: {
                        ticks: {
                            beginAtZero: true,
                            display: !isDonut(chart)
                        },
                        title: {
                            display: !isDonut(chart),
                            text: chart.yName
                        },
                        grid: {
                            display: !isDonut(chart)
                        },
                        // type: 'logarithmic',
                    },
                    x: {
                        ticks: {
                            autoSkip: true,
                            maxRotation: 0,
                            minRotation: 0,
                            display: chart.displayXLabels,
                        },
                        grid: {
                            display: false
                        },
                        title: {
                            display: !isDonut(chart),
                            text: chart.xName
                        }
                    }
                }
            }
        }));
        adjust_suggestions();
    }
}
