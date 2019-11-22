function find_reservations() {
    const customer_name = $("input[name='customer_name']").val();
    const customer_phone = $("input[name='customer_phone']").val();
    window.location = '/reservation?customer_name=' + customer_name + '&customer_phone=' + customer_phone
}

function confirm_reservations() {
    const customer_name = $('meta[name=customer_name]').attr("content");
    const customer_phone = $('meta[name=customer_phone]').attr("content");
    window.location = '/reservation?customer_name=' + customer_name + '&customer_phone=' + customer_phone + '&confirmation=' + true
}