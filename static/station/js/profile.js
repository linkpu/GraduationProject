function base_modification(){
    $('#base-modify').css("display", "none")
    $('#base-submit').css("display", "inline")
    $('#base-reload').css("display", "inline")
    $('.base-read-only').attr("readonly", false)
    $('.base-disabled').attr("disabled", false)
}

function num_modification(){
    $('#num-modify').css("display", "none")
    $('#num-submit').css("display", "inline")
    $('#num-reload').css("display", "inline")
    $('.num-read-only').attr("readonly", false)
    $('.num-disabled').attr("disabled", false)
}

function form_reload(){
    window.location.reload()
}

$("#base-info").submit(function (e) {
    e.preventDefault()
    var csrf = $("input[name='csrfmiddlewaretoken']").val()
    var stu_name = $("#stu_name").val()
    var stu_num = $("#stu_num").val()
    var stu_birth = $("#stu_birth").val()
    var stu_sex = $("input[name='sex']:checked").val()
    var area_id = $("#area option:selected").val()
    var stu_motto = $("#stu_motto").val()
    var academy_id = $('#school option:selected').val()
    var major_id = $('#major option:selected').val()
    var reg = /^[0-9a-z][_.0-9a-z-]{0,31}@([0-9a-z][0-9a-z-]{0,30}[0-9a-z]\.){1,4}[a-z]{2,4}$/
    if(stu_name != ''){
        $.ajax({
            url: '/station/profile/',
            dataType: 'json',
            type: 'POST',
            headers: {'X-CSRFToken': csrf},
            data: {'stu_name': stu_name, 'stu_num': stu_num, 'stu_birth': stu_birth, 'stu_sex': stu_sex,
                'area_id': area_id, 'stu_motto': stu_motto, 'academy_id': academy_id, 'major_id': major_id},
            success: function (data) {
                if(data.code == 200){
                    window.location.reload()
                }
                else {
                    alert('信息提交失败!')
                }
            }
        })
    }
    else {
        alert('请规范填写信息!')
    }

});


var stu_tel = $("#stu_tel").val()

$("#stu_tel").bind("input propertychange", function(){
    var new_tel = $("#stu_tel").val()
    var value = $(".num-hidden").css("display")
    if(value == 'none'){
        $(".num-hidden").css("display", "inline")
    }
    if(new_tel == stu_tel){
        $(".num-hidden").css("display", "none")
    }
})




$("#get-code").click(function(){
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
            if(data.code==1001){
                alert('请输入正确的手机号码')
            }
        })
    }
    else
        alert('请填写正确的手机号码')
})


$("#num-info").submit(function (e) {
    e.preventDefault()
    var csrf = $("input[name='csrfmiddlewaretoken']").val()
    var stu_mail = $("#stu_mail").val()
    var new_tel = $("#stu_tel").val()
    var stu_pwd = $("#stu_pwd").val()
    var confirm_pwd = $("#confirm-pwd").val()
    var reg = /^[0-9a-z][_.0-9a-z-]{0,31}@([0-9a-z][0-9a-z-]{0,30}[0-9a-z]\.){1,4}[a-z]{2,4}$/
    if(stu_tel.match(/^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$/)){
        if(stu_mail == '' || reg.test(stu_mail)){
            if ((stu_pwd == '' && confirm_pwd == '') || stu_pwd.length >= 6){
                if (confirm_pwd == stu_pwd){
                    $.ajax({
                        url: '/station/profile/',
                        dataType: 'json',
                        type: 'POST',
                        headers: {'X-CSRFToken': csrf},
                        data: {'stu_tel': new_tel, 'stu_mail': stu_mail, 'stu_pwd': stu_pwd},
                        success: function (data) {
                            if(data.code == 200){
                                window.location.reload()
                            }
                            else {
                                alert('信息提交失败!')
                            }
                        }
                    })
                }else{
                    alert('两次密码不一致！')
                }
            }else{
                alert('密码长度不少于6位！')
            }

        }else {
            alert('请输入正确的邮箱！')
        }
    }else{
        alert('请输入正确的手机号码！')
    }
});
