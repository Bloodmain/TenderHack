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
    for (let i = 0; i < data.length; ++i) {
        let chart = data[i];
        let dataCfg = {
            labels: chart.labels,
            datasets: []
        }
        for (let dataset of chart.chart) {
            dataCfg.datasets.push({
                label: dataset.line_label,
                data: dataset.data,
                borderWidth: 1,
                backgroundColor: CHART_COLORS[dataset.color],
            });
            if (chart.type === 'pie' || chart.type === 'doughnut') {
                let randomColours = [];
                for (let j = 0; j < dataset.data.length; ++j) {
                    randomColours.push('rgb(' + getRandomInt(256) + ', ' + getRandomInt(256) + ',' + getRandomInt(256) + ')');
                }
                dataCfg.datasets.at(-1).backgroundColor = randomColours;
                console.log(randomColours)
            }
        }
        // console.log(data);
        let title = chart.title;
        carousel.append("<div class=\"carousel-item" + (i === 0 ? " active" : "") + "\">\n" +
            "                <div class=\"text-center text-vertical-center\">\n" +
            "                    <h2>" + title + "</h2>\n" +
            "                </div>\n" +
            "                <div class=\"row justify-content-md-center\">\n" +
            "                    <div class=\"col col-md-5\">\n" +
            "                        <canvas id=\"chart" + i + "\"></canvas>\n" +
            "                    </div>\n" +
            "                </div>\n" +
            "            </div>");

        ctxs.push(document.getElementById('chart' + i))
        console.log()
        charts.push(new Chart(ctxs.at(-1), {
            type: chart.type,
            data: dataCfg
        }));
    }
}
