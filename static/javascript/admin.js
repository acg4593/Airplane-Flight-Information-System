//START DOCUMENT READY
$('document').ready(function() {

    //START ON CHANGE LISTENERS
    $('#leg_instance_flight_id').change(update_leg_instance);
    $('#flight_leg_flight_number').change(update_flight_leg);
    $('#fares_flight_number').change(update_fares);
    $('#can_land_airplane_type_name').change(update_can_land);
    $('#airplane_airplane_type_name').change(update_airplane);
    $('#leg_instance_leg_date').change(update_leg_instance_leg_date);
    //END ON CHANGE LISTENERS

    //START INITIAL TABLES
    $('#leg_instance_flight_id').change();
    $('#flight_leg_flight_number').change();
    update_flight();
    $('#fares_flight_number').change();
    update_airport();
    update_airplane_type();
    $('#can_land_airplane_type_name').change();
    $('#airplane_airplane_type_name').change();
    $('#leg_instance_leg_date').change();
    update_seat_reservations();
    //END INITIAL TABLES
});
//END DOCUMENT READY

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

//START UPDATE REQUEST
function update_flight_leg() {
    const flight_number = $('#flight_leg_flight_number').children("option:selected").val();
    request('GET', '/admin/update?type=flight_leg&flight_number=' + flight_number, function(result) {
        $('#flight_leg_update').html(result.data);
    });
}

function update_leg_instance() {
    const flight_id = $('#leg_instance_flight_id').children("option:selected").val();
    request('GET', '/admin/update?type=leg_instance&flight_id=' + flight_id, function(result) {
        $('#leg_instance_update').html(result.data);
    });
}

function update_flight() {
    request('GET', '/admin/update?type=flight', function(result) {
        $('#flight_update').html(result.data);
    });
}

function update_airport() {
    request('GET', '/admin/update?type=airport', function(result) {
        $('#airport_update').html(result.data);
    });
}

function update_fares() {
    const flight_number = $('#fares_flight_number').children("option:selected").val();
    request('GET', '/admin/update?type=fares&flight_number=' + flight_number, function(result) {
        $('#fares_update').html(result.data);
    });
}

function update_airplane_type() {
    request('GET', '/admin/update?type=airplane_type', function(result) {
        $('#airplane_type_update').html(result.data);
    });
}

function update_can_land() {
    request('GET', '/admin/update?type=can_land', function(result) {
        $('#can_land_update').html(result.data);
    });
}

function update_airplane() {
    const type_name = $('#airplane_airplane_type_name').children("option:selected").val();
    request('GET', '/admin/update?type=airplane&type_name=' + type_name, function(result) {
        $('#airplane_update').html(result.data);
    });
}

function update_seat_reservations() {
    request('GET', '/admin/update?type=seat_reservation', function(result) {
        $('#seat_reservation_update').html(result.data);
    })
}

function update_leg_instance_leg_date() {
    let minVal = $('#leg_instance_leg_date').val();
    const parse = minVal.split('-');
    const min = minVal + 'T00:00:00'
    const minDate = new Date(parse[0], parse[1] - 1, parse[2]);
    const maxDate = new Date(minDate.setDate(minDate.getDate() + 1));
    const md = {dd: maxDate.getDate(), mm: maxDate.getMonth() + 1,yyyy:  maxDate.getFullYear()};
    const max = md.yyyy + '-' + md.mm+'-'+md.dd + 'T23:00:00';
    $('#leg_instance_departure_time').attr('min', min);
    $('#leg_instance_departure_time').attr('max', max);
    $('#leg_instance_arrival_time').attr('min', min);
    $('#leg_instance_arrival_time').attr('max', max);
}

//END UPDATE REQUEST

//START SELECT REQUEST

function select_flight_leg() {
    request('GET', '/admin/select?type=flight_leg',function(result) {
        $('#leg_instance_flight_id').html(result.data);
    });
}

function select_airplane() {
    request('GET', '/admin/select?type=airplane',function(result) {
        $('#leg_instance_airplane_id').html(result.data);
    });
}

function select_flight() {
    request('GET', '/admin/select?type=flight',function(result) {
        $('#flight_leg_flight_number').html(result.data);
        $('#fares_flight_number').html(result.data);
    });
}

function select_airport() {
    request('GET', '/admin/select?type=airport',function(result) {
        $('#flight_leg_departure_airport_code').html(result.data);
        $('#flight_leg_arrival_airport_code').html(result.data);
        $('#can_land_airport_code').html(result.data);
    });
}

function select_airplane_type() {
    request('GET', '/admin/select?type=airplane_type',function(result) {
        $('#can_land_airplane_type_name').html(result.data);
        $('#airplane_airplane_type_name').html(result.data);
    });
}

//END SELECT REQUEST

//START FORM SUBMIT
function submit_leg_instance() {
    const flight_id = $("#leg_instance").find("[name='flight_id']").children("option:selected").val();
    const airplane_id = $("#leg_instance").find("[name='airplane_id']").children("option:selected").val();
    const leg_date = $("#leg_instance").find("[name='leg_date']").val();
    const departure_time = $("#leg_instance").find("[name='departure_time']").val();
    const arrival_time = $("#leg_instance").find("[name='arrival_time']").val();
    request('GET', '/admin/submit?type=leg_instance&flight_id=' + 
    flight_id + '&airplane_id=' + airplane_id + '&leg_date=' + leg_date + 
    '&departure_time=' + departure_time + '&arrival_time=' + arrival_time, function(_) {
        update_leg_instance();
        update_seat_reservations();
    });
}

function submit_flight_leg() {
    console.log($('#flight_leg').find('[name="flight_number"]'))
    const flight_number = $("#flight_leg").find("[name='flight_number']").children("option:selected").val();
    const leg_number = $("#flight_leg").find("[name='leg_number']").val();
    const departure_airport_code = $("#flight_leg").find("[name='departure_airport_code']").children("option:selected").val();
    const arrival_airport_code = $("#flight_leg").find("[name='arrival_airport_code']").children("option:selected").val();
    request('GET', '/admin/submit?type=flight_leg&flight_number=' +
    flight_number + '&leg_number=' + leg_number + '&departure_airport_code=' + departure_airport_code + 
    '&arrival_airport_code=' + arrival_airport_code, function(_) {
        update_flight_leg();
        select_flight_leg();
    });
}

function submit_flight() {
    const number = $("#flight").find("[name='number']").val();
    const airline = $("#flight").find("[name='airline']").val();
    const weekdays = $("#flight").find("[name='weekdays']").val();
    request('GET', '/admin/submit?type=flight&number=' +
    number + '&airline=' + airline + '&weekdays=' + weekdays, function(_) {
        update_flight();
        select_flight();
    });
}

function submit_airport() {
    const airport_code = $("#airport").find("[name='airport_code']").val();
    const name = $("#airport").find("[name='name']").val();
    const city = $("#airport").find("[name='city']").val();
    const state = $("#airport").find("[name='state']").val();
    request('GET', '/admin/submit?type=airport&airport_code=' +
    airport_code + '&name=' + name + '&city=' + city + '&state=' + state, function(_) {
        update_airport();
        select_airport();
    });
}

function submit_fares() {
    const flight_number = $("#fares").find("[name='flight_number']").children("option:selected").val();
    const fare_code = $("#fares").find("[name='fare_code']").val();
    const amount = $("#fares").find("[name='amount']").val();
    const restrictions = $("#fares").find("[name='restrictions']").val();
    request('GET', '/admin/submit?type=fares&flight_number=' +
    flight_number + '&fare_code=' + fare_code + '&amount=' + amount + '&restrictions=' + restrictions, function(_) {
        update_fares();
    });
}

function submit_airplane_type() {
    const type_name = $("#airplane_type").find("[name='type_name']").val();
    const max_seats = $("#airplane_type").find("[name='max_seats']").val();
    const company = $("#airplane_type").find("[name='company']").val();
    request('GET', '/admin/submit?type=airplane_type&type_name=' +
    type_name + '&max_seats=' + max_seats + '&company=' + company, function(_) {
        update_airplane_type();
        select_airplane_type();
    });
}

function submit_can_land() {
    const airplane_type_name = $("#can_land").find("[name='airplane_type_name']").children("option:selected").val();
    const airport_code = $("#can_land").find("[name='airport_code']").children("option:selected").val();
    request('GET', '/admin/submit?type=can_land&airplane_type_name=' +
    airplane_type_name + '&airport_code=' + airport_code, function(_) {
        update_can_land();
    });
}

function submit_airplane() {
    const airplane_id = $("#airplane").find("[name='airplane_id']").val();
    const type_name = $("#airplane").find("[name='type_name']").children("option:selected").val();
    request('GET', '/admin/submit?type=airplane&airplane_id=' +
    airplane_id + '&type_name=' + type_name, function(_) {
        update_airplane();
        select_airplane();
    });
}

//START DELETE ITEM
function delete_row_item(item) {
    data = $(item).attr('data');
    request('Get', '/admin/delete?data=' + data, function(result) {
        parse = JSON.parse(data);
        switch(parse.type) {
            case 'leg_instance':
                update_leg_instance();
                return;
            case 'flight_leg':
                update_flight_leg();
                return;
            case 'flight':
                update_flight();
                return;
            case 'airport':
                update_airport();
                return;
            case 'fares':
                update_fares();
                return;
            case 'airplane_type':
                update_airplane_type();
                return;
            case 'can_land':
                update_can_land();
                return;
            case 'airplane':
                update_airplane();
                return;
        }
    });
}
//END DELETE ITEM

//START SEAT RESERVATION TOGGLE

function seat_reservation_toggle() {
    $('#seat_reservation_update').toggle();
}

//END SEAT RESERVATION TOGGLE