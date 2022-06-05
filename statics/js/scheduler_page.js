
function enable_add(add) {
    $(".schedule_add").attr('hidden', true);
    $(".schedule_add").attr('disabled', true);
    $(add).removeAttr('hidden');
    $(add).removeAttr('disabled');
}

function enable_delete(){
    let url = $(this).attr("href");
    let id  = $(this).attr("delete");
    
    $.ajax({
        'url': url,
        'success': function(data) {
            try {
                data = JSON.parse(data);
            }
            catch(err) {
                console.log("invalid log");
            }

            if (data['status']) {
                $("#day_schedule_" + id).remove();
            }
            else {
                alert("Couldn't delete !!!");
            } 
        }
    });
}

function get_schedule_form() {
    $(".modal").css("display", "block");
    $.ajax({
        "url": "/add_schedule_form",
        "type": "GET",
        "success": function(data) {
            $(".modal_content").html(data);

            $(".add_schedule").submit(function(e) {
                e.preventDefault();

                $.ajax({
                    "url": "/day_schedule/",
                    "type": "POST",
                    "data": $(this).serialize(),
                    "success": function(data) {
                        $("#schedule_add_day").before(data);
                        $(".day_schedule_delete").click(enable_delete);
                    }
                });
            })            
        }
    });
}

$(".schedule_controls button").click(function(){
    $(".schedule_controls button").removeClass("active");
    $(this).addClass("active");
});

$("#day_schedule").click(function(){
    $.ajax({
        "url": "/day_schedule",
        "type": "GET",
        "success": function(data) {
            let add = $("#schedule_add_day");
            $(".manager_body").html(data);
            $(".manager_body").append(add);

            enable_add(add);

            $("#schedule_add_day").click(get_schedule_form);

            $(".day_schedule_delete").click(enable_delete);
        }
    });
});

$("#schedule_add_day").click(get_schedule_form);

$(".modal").click(function(e) {
    if (e.target == $(this)[0]) {
        $(this).css("display", "none");
    }
});

$("#close").click(function() {
    $(".modal").css("display", "none");
});