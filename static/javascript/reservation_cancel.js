function cancel_reservation(item) {
    data = $(item).attr('data');
    if (confirm('Cancel Reservation?')) {
        request('GET', '/cancel_reservation_for?data=' + data, function(result) {
            if(result.status == 'success') {
                location.reload()
            } else{
                alert('Failed to Cancel Reservation!')
            }
        });
    }
    else{ 

    }
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