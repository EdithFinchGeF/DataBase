$(document).ready(function () {
    function click_grade_search () { 
        cname = $('#cname').val()
        page = 1
        data = {
            "cname":cname,
            "page":page,
        }
        $.ajax({
            type: "POST",
            url: search_grade_url,
            data: JSON.stringify(data),
            contentType: "application/json;charset=uft-8",
            success: function (response) {
                $("tbody").html(response.html)
                pages = response.pages
                bootoast( {
                    message : response.message,
                    type: response.type,
                    position:'right-top',
                    timeout : 5,
                    })
            }
        }); 
    }

    $(document).on('click','#search_grade',click_grade_search)
       

});


