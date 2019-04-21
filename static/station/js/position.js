// 省级select id使用province
// 市级select id使用city
// 区县级select id使用area

// 省级框选中事件
$('#province').change(function (){
    var province_id = $('#province option:selected').val();
    $.get("/academy/province_change/" + province_id + "/", function (data) {
        if (data.code = 200){
            var city_select = $('#city')
            var area_select = $('#area')
            city_select.empty()
            area_select.empty()
            city_select.append("<option value='" + data.cities[0].code_id + "' selected>" + data.cities[0].area_name + "</option>\n")
            for (var index = 1; index < data.cities.length; index++){
                city_select.append("<option value='" + data.cities[index].code_id + "'>" + data.cities[index].area_name + "</option>\n")
            }
           area_select.append("<option value='" + data.areas_[0].code_id + "' selected>" + data.areas_[0].area_name + "</option>\n")
            for (var index = 1; index < data.areas_.length; index++){
                area_select.append("<option value='" + data.areas_[index].code_id + "'>" + data.areas_[index].area_name + "</option>\n")
            }
        }
    })
});

$('#city').change(function () {
    var city_id = $('#city option:selected').val();
    $.get("/academy/city_change/" + city_id + "/", function (data) {
        if (data.code = 200){
            var area_select = $('#area')
            area_select.empty()
            area_select.append("<option value='" + data.areas_[0].code_id + "' selected>" + data.areas_[0].area_name + "</option>\n")
            for (var index = 1; index < data.areas_.length; index++){
                area_select.append("<option value='" + data.areas_[index].code_id + "'>" + data.areas_[index].area_name + "</option>\n")
            }
        }
    })
});