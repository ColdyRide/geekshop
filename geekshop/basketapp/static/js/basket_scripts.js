window.onload = function () {
    $('.basket_list').on('click', 'input[type="number"]', function () {
        var t_href = event.target;

        $.ajax({
            url: "/basket/edit/" + t_href.name + "/" + t_href.value + "/",
            success: function (data) {
                console.log(data.main_links)
                console.log($('.hero-white'))
                $('.basket_list').html(data.result);
                $('.hero-white').html(data.main_links)
                // window.location.reload()
            },
        });

        event.preventDefault();
    });
}