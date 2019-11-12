$('document').ready(function() {
    $('#flight_id').change(function() {
        console.log('leg_instance_update');
        const flight_id = $(this).children("option:selected").val();
        request('/admin/leg_instance_update_get?flight_id=' + flight_id, function(result) {
            console.log(result);
            $('#leg_instance_update').html(result.data)
        })
    });
    $('#flight_number').change(function() {
        console.log('flight_leg_update');
        const flight_number = $(this).children("option:selected").val();
        request('/admin/flight_leg_update_get?flight_number=' + flight_number, function(result) {
            console.log(result);
            $('#flight_leg_update').html(result.data)
        })
    });
})


function request(url, onSuccess) {
    console.log(url);
    const req = new XMLHttpRequest();
    req.open('GET', url, true);
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
            onSuccess(data);
        }
    }
    req.send();
}