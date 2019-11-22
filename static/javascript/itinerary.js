function load_itinerary() {
    const customer_name = $("input[name='customer_name']").val();
    const customer_phone = $("input[name='customer_phone']").val();
    window.location = '/itinerary?customer_name=' + customer_name + '&customer_phone=' + customer_phone
}