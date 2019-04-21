$('#new-gallery').click(function () {
    $('#new_form').css('display', 'inline')
})

function is_image(file) {
    if(file.name == "") {
		return false;
	}
	else {
		/*图片类型正则验证*/
		var imgStr = /\.(jpg|jpeg|png|bmp|BMP|JPG|PNG|JPEG)$/
		if(!imgStr.test(file.name)) {
			return false
		}
		// else {
		// 	/*图片大小*/
		// 	var imagSize = file.size;
		// 	if(imagSize < (1024 * 1024 * maxsize)) {
		// 		return true
		// 	} else {
		// 		alert(imgFile.name + "大小不能超过" + maxsize + "M")
		// 		return false
		// 	}
		// }
		return true
	}
}

function showPhoto(source) {
    var file = source.files[0];
    if (is_image(file)){
        if (window.FileReader) {
            var fr = new FileReader();
            fr.onloadend = function (e) {
                $("#headphoto").attr("src",e.target.result);
            };
            fr.readAsDataURL(file);
        }
    }
}

function changeHeader(){
    $("[id=headfile]").click()
}

// $('#gallery_submit').click(function () {
//     var csrf = $("input[name='csrfmiddlewaretoken']").val()
//     var gallery_id = $('#gallery_id').val()
//     var gallery_name = $('#gallery_name').val()
//     var activity_id = $('#activity option:selected').val()
//     var gallery_describe = $('#discribe').val()
//     var gallery_permission = $('#permission option:selected').val()
//     var gallery_data = new FormData()
//     if (activity_id == 'none'){
//         activity_id = ''
//     }
//     if(is_image(file)){
//         gallery_data.append('head_photo', file)
//     }
//     gallery_data.append('gallery_id', gallery_id)
//     gallery_data.append('gallery_name', gallery_name)
//     gallery_data.append('gallery_describe', gallery_describe)
//     gallery_data.append('gallery_permission', gallery_permission)
//     gallery_data.append('activity_id', activity_id)
//     $.ajax({
//         url: '/association/gallery_list//',
//         dataType: 'json',
//         type: 'POST',
//         contentType: false,
//         processData: false,
//         headers: {'X-CSRFToken': csrf},
//         data: gallery_data,
//         success: function (data) {
//             if(data.code == 200){
//                 var gallery = data.gallery
//             }
//             else {
//                 alert(data.msg)
//             }
//         },
//         error: function () {
//             alert('创建失败')
//         }
//     })
// })


function enter_gallery(g_id) {
    $('#gallery_title').attr('g-id', g_id)
    $('.photo').remove()
    $.get('/association/gallery/' + g_id + '/', function (data) {
        if (data.code == 200){
            $('#gallery_title').text(data.gallery_name)
            var imgs = data.images
            for(var i=0; i<imgs.length; i++){
                // $('#new-img').after("<div class='span3 img-container photo'><div class='img-box'><span class='icon trash'><i class='gallery-trash'></i></span><img height='200px' width='225px' src='/media/" + imgs[i].path + "'/></div></div>")
                $('#photos').append("<a class='wall-item photo'><img src='" + imgs[i].path + "' /><h2>Cursus cursus proin auctor in in ac, nunc, tortor</h2></a>")
            }
        }
    })

}

$(function(){
    $('.wall').jaliswall({ item: '.article' });
});

function upload_file(img) {
    var img = img.files[0];
    if (is_image(img)){
        // if (window.FileReader) {
        //     var fr = new FileReader();
        //     fr.onloadend = function (e) {
        //         $("#headphoto").attr("src",e.target.result);
        //     };
        //     fr.readAsDataURL(file);
        // }
        var csrf = $("input[name='csrfmiddlewaretoken']").val()
        var g_id = $('#gallery_title').attr('g-id')
        if(g_id != ''){
            var img_form = new FormData()
            img_form.append('photo', img)
            alert(33333)
            $.ajax({
                url: '/association/gallery/' + g_id + '/',
                dataType: 'json',
                type: 'POST',
                contentType: false,
                processData: false,
                headers: {'X-CSRFToken': csrf},
                data: img_form,
                success: function (data) {
                    if(data.code == 200){
                        $('#new-img').after("<div class='span3 img-container photo'><div class='img-box'><span class='icon trash'><i class='gallery-trash'></i></span><img height='200px' width='225px' src='/media/" + data.photo.path + "'/></div></div>")
                    }
                    else {
                        alert(data.msg)
                    }
                },
                error: function () {
                    alert('创建失败')
                }
            })
        }
        else {
            alert('请先选择相册')
        }
    }
    $('#image').val('')
}

function upload_img(){
    $("[id=image]").click()
}