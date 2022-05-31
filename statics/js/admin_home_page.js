$("#add_station").click(function(e) {
    e.preventDefault();
    $(".modal").css('display', 'block');

    $.ajax({
        "url": $(this).attr('href'),
        "type": "GET",
        "success": function(data) {
            // alert(data);
            $('.modal_content').html(data);

            $(".submit_add_station").click(function() {
            
                let name = $("#station_name").val();
                let location = $("#station_location").val();
                let desc = $("#station_description").val();
            
                $.ajax({
                    "url": '/add_station/'+name+'/'+location+'/'+desc,
                    "success": function(data) {   

                        try {
                            data = JSON.parse(data);

                            $(".message_box").html(data['message']);

                            if (data['status']) {
                                $('input, textarea').val('');
                            }
                        }
                        catch (err) {
                            console.log("invalid log !!!")
                        }
                    }
                });
            });
        }
    });
});

$(".modal").click(function(e) {
    if (e.target == $(this)[0]) {
        $(this).css("display", "none");
    }
});

$("#close").click(function() {
    $(".modal").css("display", "none");
});