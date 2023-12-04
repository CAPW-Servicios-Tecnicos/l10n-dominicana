$(function () {
    var search_result = $("#search_result").val();
    console.log('Search result:', search_result);

    if (search_result) {
        setTimeout(function () {
            $(".alert-success").fadeOut(1000);
        }, 10000);
    }
});
