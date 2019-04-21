function get_vercode() {
    var tel = $('#stu_tel').val()
    if(tel.match(/^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$/))
    {
        $.get('/station/get_vercode/', {'stu_tel': tel}, function (data) {
            if(data.code==200){
                var seconde = 60
                $('#verbtn').attr({"disabled": "disabled"})
                var interval = setInterval(function () {
                    var text = "重新获取(" + seconde + ")"
                    $('#verbtn').text(text)
                    seconde = seconde - 1
                    if(seconde === 0){
                        $('#verbtn').removeAttr("disabled")
                        $('#verbtn').text("获取验证码")
                        clearInterval(interval)
                    }
                }, 1000)
            }
            else {
                alert(data.error_code)
            }
        })
    }
    else
        alert('请输入正确的手机号码')
}