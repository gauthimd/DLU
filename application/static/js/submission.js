function check_status() {
    window.event.preventDefault();
    $.ajax({
        type: 'GET',
        url: "/check-status/",
        success: function (data, status, request) {
            $('#load_icon_1').hide();
        },
        error: function (data, status, request) {
            $('#load_icon_1').hide();
        }
    });
}



function get_status_data() {
    location.reload();
}

function get_status_data_without_page_reload() {

}

