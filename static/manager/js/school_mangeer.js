$.get('/api/get_provinces/', function (provinces_data) {
    if (provinces_data.code == 200) {
        var provinces = provinces_data.provinces
        var school_area = $('#school_area')
        for (var index = 0; index < provinces.length; index++) {
            school_area.append("<option value='" + provinces[index].code_id + "'>" + provinces[index].area_name + "</option>\n")
        }
    }
});

$('#school_area').change(function (){
    var province_id = $('#school_area option:selected').val()
    $.get("/academy/school_area_change/" + province_id + "/", function (data) {
        if (data.code = 200){
            var school_select = $('#school')
            var schools = data.schools
            school_select.empty()
            school_select.append("<option value='' class='default'>--学校--</option>\n")
            for (var index = 0; index < schools.length; index++){
                school_select.append("<option value='" + schools[index].id + "'>" + schools[index].school_name + "</option>\n")
            }
        }
    })
});


$("#school").change(function () {
    var school_id = $('#school option:selected').val()
    $.get("/api/school_by_id/" + school_id + "/", function (data) {
        if (data.code = 200){
            var school  = data.school
            $('#id_school_num').val(school.school_num)
            $('#id_school_pwd').val(school.school_pwd)
            $('#id_school_tel').val(school.school_tel)
        }
    })
});


$('#academy_form').submit(function (e) {
    e.preventDefault()
    var school_id = $('#school option:selected').val();
    var school_pwd = $('#id_school_pwd').val()
    var school_tel = $('#id_school_tel').val()
    var csrf = $("input[name='csrfmiddlewaretoken']").val()
    $.ajax({
        url: '/manager/update_school/' + school_id + '/',
        dataType: 'json',
        type: 'POST',
        headers: {'X-CSRFToken': csrf},
        data: {'school_tel': school_tel, 'school_pwd': school_pwd},
        success: function (data) {
            if(data.code == 200) {
                alert('院校信息更新成功!')
                window.location.reload()
            }
            else {
                alert(data.msg)
            }
        }
    })
})