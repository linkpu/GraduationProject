function login_info(){
    $.get('/station/login_info/', function (data) {
        if (data.code == 200)
        {
            $("#is_login>a").html(data.username)
            $("#not_login").css('display', 'none')
            $("#is_login").css('display', 'inline')
        }
    })
}