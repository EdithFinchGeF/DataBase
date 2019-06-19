$(document).ready(function () {
    var pages = 0
    var page = 1
    
    function show_page_button(){
        $('#button_group').show()
        $nextpage = $('#nextpage')
        $lastpage = $('#lastpage')
        if (page >= pages || pages === 0)
            $nextpage.hide()
        else
            $nextpage.show()
        if (page == 1)
            $lastpage.hide()
        else
            $lastpage.show()    
    }
    
    $(document).on('click','#search_grade',function () {
        var text = $('.breadcrumb-item.active').text();
        var sname = $("#sname").val() 
        var sno= $("#sno").val() 
        var cname = $("#cname").val() 
        page = 1
        var data ={
            'sno' : sno ,
            'sname' : sname ,
            'cname' : cname,
            'page' : page,
        }
        $.ajax({
            type: "POST",
            url: search_grade_url,
            data: JSON.stringify(data),
            contentType: "application/json;charset=uft-8",
            success: function (data) {
                bootoast({
                    message:data.message,
                    type:data._type,
                    position:'right-top',
                    timeout:5,
                })
                $('tbody').html(data.html);
                pages = data.pages
                show_page_button()
            }
        });
    });

    $(document).on("click","#search_student",function (){
        var sname = $('#sname').val()
        var sno = $('#sno').val()
        var sex = $('#sex').val()
        var dname = $('#dname').val()
        var dormno = $('#dormno').val()
        var page = 1
        data = {
            "sname":sname,
            "sno":sno,
            "sex":sex,
            "dname":dname,
            "dormno":dormno,
            "page": page
        }
        $.ajax({
            type: "POST",
            url: search_student_info_url,
            data: JSON.stringify(data),
            contentType: "application/json;charset=uft-8",
            success: function (response) {
                $('tbody').html(response.html)
                bootoast({
                    message:response.message,
                    type:response._type,
                    position:'right-top',
                    timeout:5,
                })
                pages = response.pages
                show_page_button()
            }
        });
    })



});