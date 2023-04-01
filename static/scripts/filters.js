$.get('/api/categories', {}, function (data) {
    let categories = data[0]['categories'];
    let select_form = $('#list-categories');
    for (let i = 0; i < categories.length; ++i) {
        select_form.append('<option>' + categories[i] + '</option>');
    }
})

$(document).ready(function () {
    let d = new Date()
    $('#dateEnd').attr("value", d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" +
        ("0" + d.getDate()).slice(-2));
})
$('#applyFilters').click(function () {
    let categories;
})
