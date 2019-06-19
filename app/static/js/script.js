$(document).ready(function () {
    var ENTER_KEY = 13;
    var ESC_KEY = 27;
    

    var csrftoken = $('meta[name=csrf-token]').attr('content')

    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
    })
    
    $(window).bind('hashchange', function () { 
        var hash = window.location.hash.replace('#','')
        var url = null
        if (hash === 'change_passwd') {
            url = change_passwd_url;
        }else if(hash ==='grade_search'){
            url = search_grade_url;
        }else if(hash === 'manage_student'){
            url = manage_student_url;
        }else if(hash === 'manage_student_grade'){
            url = manage_student_grade_url;
        }else if(hash === "manage_course"){
            url = manage_course_url;
        }else{
            url = search_student_info_url;
        }
        var $checked = $('.list-group-item.list-group-item-action').filter(function(){
            if ( $(this).attr('href') === '#'+ hash)
                return true
        })
        
        $checked.addClass("active")
        $checked.siblings('.list-group-item.list-group-item-action').removeClass('active')

        $.ajax({
            type: "GET",
            url: url,
            success: function (data) {
                $('#main').hide().html(data).fadeIn(700);
            }
        });
    });



    
    if (window.location.hash === '') {
        window.location.hash = '#intro'; // home page, show the default view
    } else {
        $(window).trigger('hashchange'); // user refreshed the browser, fire the appropriate function
    }


    

    $(document).on('click','#changePasswd',function (e) { 
        var new_passwd = $('#new_passwd').val()
        var comfirmed_passwd = $('#comfirmed_passwd').val()
        var old_passwd = $('#old_passwd').val()

        error = null
        if (old_passwd === '')
            error = '原密码未填'
        else if(new_passwd === '')
            error = '新密码未填'
        else if(comfirmed_passwd === '')
            error = '确认密码未填'
        else if  ( new_passwd != comfirmed_passwd )
            error = '两次输入密码不一致'
        
        if (error != null){
            bootoast( {
                message : error,
                type: 'warning',
                position:'right-top',
                timeout:5,
                })
            return
        }

        var data = {
            'old_passwd': old_passwd,
            'new_passwd': new_passwd,
            'comfirmed_passwd': comfirmed_passwd
        }
        $.ajax({
            type: "POST",
            url: change_passwd_url,
            data: JSON.stringify(data),
            contentType: "application/json;charset=uft-8",
            success: function (data) {
                bootoast( {
                message : data.message,
                type: data._type,
                position:'right-top',
                timeout : 5,
                })
                $(window).trigger('hashchange')
            }
        });
        
    });

});


