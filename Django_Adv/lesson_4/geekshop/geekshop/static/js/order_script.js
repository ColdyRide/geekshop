window.onload = function () {
    var _quantity, _price, orderitem_num, delta_quantity, quantity_arr, price_arr,
        order_total_quantity = 0,
        order_total_cost = 0,
        TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());

    function getArray() {
        TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
        quantity_arr = [];
        price_arr = [];
        for (let i = 0; i < TOTAL_FORMS; i++) {
            _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
            _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));

            if (_price) {
                price_arr[i] = _price;
            } else {
                price_arr[i] = 0;
            }
            if (isNaN(_quantity)) {
                quantity_arr[i] = 0;
                price_arr[i] = 0;
            } else {
                quantity_arr[i] = _quantity;
            }
        }
    }

    function orderSummaryUpdate() {
        getArray();
        order_total_cost = price_arr.reduce((a, b) => a + b, 0)
        order_total_quantity = quantity_arr.reduce((a, b) => a + b, 0)

        $('.order_total_cost').html(order_total_cost.toFixed(2).toString().replace('.', ','));
        $('.order_total_quantity').html(order_total_quantity.toString());
    }

    orderSummaryUpdate();


    $('.order_form').on('click', 'input[type="number"]', function () {
        const target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (price_arr[orderitem_num]) {
            orderSummaryUpdate();
        }
    })

    $('.order_form').on('click', 'input[type="checkbox"]', function () {
        const target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));
        if (target.checked) {
            orderSummaryUpdate();
        }
    })


    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitems',
        added: () => $('.order_form select').last().change(ajaxUpdate),
        removed: deleteOrderItem
    })

    function deleteOrderItem() {
        TOTAL_FORMS -= 1
        orderSummaryUpdate();
    }

    function ajaxUpdate() {
        let target = event.target;

        let form_num = target.name.replace('orderitems-', '').replace('-product', ''),
            new_form_price = document.querySelector(`.orderitems-${form_num}-price`),
            new_form_max_quantity = document.querySelector(`input[name=orderitems-${form_num}-quantity]`);
        new_form_max_quantity.value = 0;


        $.ajax({
            data: {
                'product_id': target.value
            },
            success: function (data) {
                if ((data.price) && (data.quantity)) {
                    new_form_price.textContent = parseFloat(data.price).toFixed(2).replace('.', ',');
                    new_form_max_quantity.setAttribute('max', data.quantity)
                    orderSummaryUpdate()
                }
            },
        });

        event.preventDefault();
    }


    $('.order_form select').change(ajaxUpdate);

}
