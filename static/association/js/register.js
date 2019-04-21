// $("#register").submit(function (e) {
//     e.preventDefault()
//     var csrf = $("input[name='csrfmiddlewaretoken']").val()
//     var password = $('#password').val()
//     var password1 = $('#confirm-pwd').val()
//     if(password == password1){
//         var form_data = new FormData()
//         var apply_file = $('#apply-file')[0].files[0]
//         form_data.append('apply_file', apply_file)
//         form_data.append('school_id', $('#school option:selected')).val()
//         form_data.append('association_name', $('#association_name').val())
//         form_data.append('association_desc', $('#association_desc').val())
//         form_data.append('association_pwd', $('#password').val())
//         $.ajax({
//             url: '/association/register/',
//             type: 'POST',
//             data: form_data,
//             headers: {'X-CSRFToken': csrf},
//             processData: false,  // tell jquery not to process the data
//             contentType: false, // tell jquery not to set contentType
//             success: function(data) {
//
//             }
//
//         })
//     }
//     else {
//         alert('两次密码不一致')
//     }
//
// })