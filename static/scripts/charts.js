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

const ctx = document.getElementById('myChart');
const ctx2 = document.getElementById('myChart2');
const ctx3 = document.getElementById('myChart3');
const DATA_COUNT = 12;
const labels = [];
for (let i = 0; i < DATA_COUNT; ++i) {
    labels.push(i.toString());
}
const datapoints = [0, 20, 20, 60, 60, 120, NaN, 180, 120, 125, 105, 110, 170];

let datapoints2 = []
for (let i = 0; i < 100; ++i) {
    datapoints2.push(i);
}

new Chart(ctx, {
    type: 'bar',
    plugins: [
        ChartRegressions
    ],
    data: {
        labels: ['hey', 'meow', '34', '24', 'now', 'dsf', '123', 'sg', 'pred_1', 'pred_2', 'pred_3', 'pred_4'],
        datasets: [{
            backgroundColor: 'rgb(54, 162, 235, 0.5)',
            label: 'label',
            data: [234, 234, 1, 23, 500, 13, 0, 10, 0, 0, 0, 0],
            borderWidth: 1,
            regressions: {
                type: "polynomial",
                line: {color: "blue", width: 3},
                extendPredictions: true,
                sections: [
                    {
                        startIndex: 0,
                        endIndex: 7,
                        line: {color: "red"}
                    },
                    {
                        type: "copy",
                        copy: {fromSectionIndex: 0, overwriteData: "all"},
                        startIndex: 7
                    }
                ]
            }
        }]
    }
});

new Chart(ctx2, {
    type: 'bar',
    data: {
        labels: ['Red'],
        datasets: [{
            label: '# of Votes',
            data: [12],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

data = {
    labels: ['hey', 'meow', '34', '24', 'now'],
    datasets: [
        {
            label: 'Dataset 1',
            data: [20, 10, 30, 1, 20, 3],
            borderColor: CHART_COLORS.red,
        },
        {
            label: 'Dataset 2',
            data: [5, 10, 2, 0, 32, 7],
            borderColor: CHART_COLORS.blue,
        }
    ]
};

new Chart(ctx3, {
    type: 'line',
    data: data
});

