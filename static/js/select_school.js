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