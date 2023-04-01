$.get('/api/categories', {}, function (data) {
    let categories = data['categories'];
    let select_form = $('#list-categories');
    for (let i = 0; i < categories.length; ++i) {
        select_form.append('<option>' + categories[i] + '</option>');
    }
})

$.get('/api/regions', {}, function (data) {
    let regions = data['regions'];
    console.log(regions)
    let select_form = $('#list-regions');
    for (let i = 0; i < regions.length; ++i) {
        select_form.append('<option>' + regions[i] + '</option>');
    }
})

$(document).ready(function () {
    let d = new Date()
    $('#dateEnd').attr("value", d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" +
        ("0" + d.getDate()).slice(-2));
})
$('#applyFilters').click(function () {
    let categories = $("#categories-datalist")
})
