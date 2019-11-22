function navigate(target) {
    id = $(target).attr('target');
    $('#navigation_content').children().removeClass('show').addClass('hide');
    $(id).toggleClass('show hide');
}