function navigate(target) {
    id = $(target).attr('target');
    $('#navigation_content').children().removeClass('show').addClass('hide');
    $(id).toggleClass('show hide');
}

function get_flight_roster() {
    const flight_number = $("#roster_query").find("[name='flight_number']").val();
    const leg_number = $("#roster_query").find("[name='leg_number']").val();
    const month = $("#roster_query").find("[name='month']").children("option:selected").val();
    const year = $("#roster_query").find("[name='year']").val();
    request('GET', '/roster_request?' + 
        'flight_number=' + flight_number + 
        '&leg_number=' + leg_number + 
        '&month=' + month + 
        '&year=' + year, function(result) {
        $('#roster_placeholder').html(result.data)
    });
}

function get_flight_schedule() {
    const airline = $("#schedule_query").find("[name='airline']").val();
    const departure_city = $("#schedule_query").find("[name='departure_city']").val();
    const arrival_city = $("#schedule_query").find("[name='arrival_city']").val();
    const month = $("#schedule_query").find("[name='month']").children("option:selected").val();
    const year = $("#schedule_query").find("[name='year']").val();
    request('GET', '/schedule_request?' + 
        'airline=' + airline + 
        '&departure_city=' + departure_city + 
        '&arrival_city=' + arrival_city +
        '&month=' + month + 
        '&year=' + year, function(result) {
        $('#schedule_placeholder').html(result.data)
    });
}

function get_flight_report() {
    const airline = $("#report_query").find("[name='airline']").val();
    const month = $("#report_query").find("[name='month']").children("option:selected").val();
    const year = $("#report_query").find("[name='year']").val();
    request('GET', '/report_request?' + 
        'airline=' + airline + 
        '&month=' + month + 
        '&year=' + year, function(result) {
        $('#report_placeholder').html(result.data)
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