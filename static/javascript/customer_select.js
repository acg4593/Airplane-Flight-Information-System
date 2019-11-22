function reserve_continue() {
    const leg_id = $('title').text();
    const seat_number = $("input[name='seat_number']:checked").val();
    const customer_name = $("input[name='customer_name']").val();
    const customer_phone = $("input[name='customer_phone']").val();
    const fare_code = $("input[name='fare_code']:checked").val();
    request('GET', '/reserve?' + 
    'leg_id=' + leg_id + 
    '&seat_number=' + seat_number + 
    '&customer_name=' + customer_name + 
    '&customer_phone=' + customer_phone +
    '&fare_code=' + fare_code, function(response) {
        if(response.status == 'success') {
            alert('Seat #' + seat_number + ' has been added!  Please confirm your reservation!')
        }
        else{
            alert('Seat #' + seat_number + ' Failed to be added...')
        }
    });
}

//START REQUEST
function request(type, url, onSuccess) {
    console.log(type, url);
    const req = new XMLHttpRequest();
    req.open(type, url, true);
    req.onreadystatechange = function(e) {
        if(req.readyState !== 4) {
            return;
        }
        if ([200, 304].indexOf(req.status) === -1) {
            console.warn('Error! XHR failed.');
            return;
        }
        else {
            const data = JSON.parse(e.target.responseText);
            console.log(data);
            onSuccess(data);
        }
    }
    req.send();
}
//END REQUEST