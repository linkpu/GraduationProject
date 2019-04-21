$('#register-form').submit(function (e) {
    e.preventDefault()
    alert(1)
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $(this).ajaxSubmit({
        url: '/student/stu_register/',
        type: 'POST',
        headers: {'X-CSRFToken': csrf},
        dataType: 'json',
        success: function (data) {
            if(data.code == 200){

            }
        }
    })

})