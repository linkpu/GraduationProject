function association_login() {
    $.get('/association/is_login/', function (association_data) {
        if(association_data.code == 200){
            $('#log-info').attr('value', association_data.association_id)
            $('#log-info').attr('data-toggle', 'dropdown')
            $('#log-info').text(association_data.association_name)
            }
    })
}

function logout() {
    $.get('/association/logout/', function (data) {
        if(data.code == 200){
            // $('#log-info').attr('value', '')
            // $('#log-info').attr('data-toggle', '')
            // $('#log-info').text('请登录')
            window.location.replace('/association/login/')
        }
    })
}