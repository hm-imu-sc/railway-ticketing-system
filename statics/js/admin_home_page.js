$("#add_station").click(function(e) {
    e.preventDefault();
    $(".modal").css('display', 'block');

    $.ajax({
        "url": $(this).attr('href'),
        "type": "GET",
        "success": function(data) {
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

$("#add_train").click(function(e) {
    e.preventDefault();
    $(".modal").css('display', 'block');

    $.ajax({
        "url": $(this).attr('href'),
        "type": "GET",
        "success": function(data) {
            $('.modal_content').html(data);

            $(".add_train").submit(function(e){
                e.preventDefault();

                $.ajax({
                    "url": $(this).attr('action'),
                    "type": "GET",
                    "data": $(this).serialize(),
                    "success": function(data) {

                        try {
                            data = JSON.parse(data);
                            $(".message_box").html(data['message']);
                            $('.modal_content').scrollTop($('.modal_content').height());
                        }
                        catch (err) {
                            console.log("invalid log !!!")
                        }
                    }
                });
            });
        }
    })
})

$(".modal").click(function(e) {
    if (e.target == $(this)[0]) {
        $(this).css("display", "none");
    }
});

$("#close").click(function() {
    $(".modal").css("display", "none");
});