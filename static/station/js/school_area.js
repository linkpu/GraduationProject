// 省份select id 使用school_area
// 学校select id 使用school
// 专业select id 使用major

$('#school_area').change(function (){
    var province_id = $('#school_area option:selected').val();
    $.get("/academy/school_area_change/" + province_id + "/", function (data) {
        if (data.code = 200){

            var school_select = $('#school')
            var major_select = $('#major')
            console.log(major_select)
            major_select.empty()
            school_select.empty()
            major_select.append("<option value='' class='default'>--专业--</option>\n")
            school_select.append("<option value='' class='default'>--学校--</option>\n")
            for (var index = 0; index < data.schools.length; index++){
                school_select.append("<option value='" + data.schools[index].id + "'>" + data.schools[index].school_name + "</option>\n")
            }
        }
    })
});


$("#school").change(function () {
    var school_id = $('#school option:selected').val();
    $.get("/academy/school_change/" + school_id + "/", function (data) {
        if (data.code = 200){
            var major_select = $('#major')
            major_select.empty()
            major_select.append("<option value='' class='default'>--专业--</option>\n")
            for (var index = 0; index < data.majors.length; index++){
                major_select.append("<option value='" + data.majors[index].id + "'>" + data.majors[index].major_name + "</option>\n")
            }
        }
    })
});