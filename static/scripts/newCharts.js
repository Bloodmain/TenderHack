$(document).ready(() => $('.carousel').carousel());

const CHART_COLORS = {
    red: 'rgb(255, 99, 132)',
    orange: 'rgb(255, 159, 64)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)'
};


function update_charts(data) {
    let carousel = $('.carousel');
    for (let i = 0; i < data.length; ++i) {
        let chart = data[i];
        data = {
            labels: chart.labels,
            datasets: []
        }
        for (let dataset in chart.chart) {
            data.datasets.push({
                label: dataset.line_label,
                data: dataset.data,
                borderWidth: 1,
                backgroundColor: CHART_COLORS[dataset.color],
            });
        }

        let title = chart.title;
        carousel.append("<div class=\"carousel-item\">\n" +
            "                <div class=\"text-center text-vertical-center\">\n" +
            "                    <h2>" + title + "</h2>\n" +
            "                </div>\n" +
            "                <div class=\"row justify-content-md-center\">\n" +
            "                    <div class=\"col col-md-5\">\n" +
            "                        <canvas id=\"chart" + i + "\"></canvas>\n" +
            "                    </div>\n" +
            "                </div>\n" +
            "            </div>");
        new Chart(document.getElementById('chart' + i), {
            type: chart.type,
            data: data
        });
    }
}
