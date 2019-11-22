//START DOCUMENT READY
$('document').ready(function() {

    update_flights_viewport();

});
//END DOCUMENT READY


function get_flight_viewport_form() {
    FROM = $('#viewport_query').find("[name='from']").val();
    TO = $('#viewport_query').find("[name='to']").val();
    DEPART = $('#viewport_query').find("[name='depart']").val();
    update_flights_viewport(FROM, TO, DEPART);
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

//START UPDATE REQUEST

function update_flights_viewport(FROM='', TO='', DEPART='') {
    request('GET', '/customer/search?from=' + FROM + '&to=' + TO + '&depart=' + DEPART, function(result) {
        $('#flights_viewport').html(result.data);
    });
}

//END UPDATE REQUEST