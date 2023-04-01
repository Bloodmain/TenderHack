$.get('/api/categories', {}, function (data) {
    let categories = data['categories'];
    let select_form = $('#list-categories');
    for (let i = 0; i < categories.length; ++i) {
        select_form.append('<option>' + categories[i] + '</option>');
    }
})

$.get('/api/regions', {}, function (data) {
    let regions = data['regions'];
    let select_form = $('#list-regions');
    for (let i = 0; i < regions.length; ++i) {
        select_form.append('<option>' + regions[i] + '</option>');
    }
})

$(document).ready(function () {
    let d = new Date()
    $('#dateEnd').attr("value", d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" +
        ("0" + d.getDate()).slice(-2));
    start_charts_update();
})

function get_filters() {
    return {
        'inn': window.location.pathname.split('/').at(-1),
        'category': $("#categories-datalist").val(),
        'region': $("#regions-datalist").val(),
        'dateStart': $("#dateStart").val(),
        'dateEnd': $("#dateEnd").val()
    }
}

$('#applyFilters').click(start_charts_update);

function start_charts_update() {
    $.get('/api/charts/', get_filters(), update_charts);
}
