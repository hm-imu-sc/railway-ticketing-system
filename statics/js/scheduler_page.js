
function enable_delete() {
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

function enable_week_schedule_delete() {

    let id = $(this).attr("delete");

    $.ajax({
        "url": $(this).attr("href"),
        "success": function(data) {
            try {
                data = JSON.parse(data);
            }
            catch (err) {
                console.log("Invalid log !!!");
            }

            if (data["status"]) {
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
                        let id = $($(data).find(".day_schedule_delete")[0]).attr('delete');
                        $(`.day_schedule_delete[delete='${id}']`).click(enable_delete);
                    }
                });
            })            
        }
    });
}

function get_week_day_schedule_form() {
    $(".modal").css("display", "block");
    let url = $(this).attr("href");

    $.ajax({
        "url": url,
        "success": function(data) {
            $(".modal_content").html(data);

            $(".add_schedule").submit(function(e) {
                e.preventDefault();

                $.ajax({
                    "url": $(this).attr("action"),
                    "type": "POST",
                    "data": $(this).serialize(),
                    "success": function(data) {

                        // alert(data);

                        $("#schedule_add_day").before(data);
                        let id = $($(data).find(".day_schedule_delete")[0]).attr('delete');
                        $(`.day_schedule_delete[delete='${id}']`).click(enable_week_schedule_delete);
                    }
                });
            })    
        }
    });
}

function enable_reverter() {
    $.ajax({
        "url": $(this).attr("href"),
        "success": function(data) {
            let reverter = $(".revert");
            $(".day_schedules").html(data);
            $(".day_schedule_delete").click(enable_week_schedule_delete);
            $(".schedule_add").click(get_week_day_schedule_form);
            $(".day_schedules").append(reverter);
            $(".revert").click(enable_reverter);

        }
    });
}

$(".schedule_controls button").click(function() {
    $(".schedule_controls button").removeClass("active");
    $(this).addClass("active");
});

$("button#day_schedule").click(function() {
    $.ajax({
        "url": $(this).attr("href"),
        "type": "GET",
        "success": function(data) {
            $(".manager_body").html("<div class='day_schedules'></div>");
            
            $(".day_schedules").html(data);

            $("#schedule_add_day").click(get_schedule_form);
            $(".day_schedule_delete").click(enable_delete);
        }
    });
});

$("button#week_schedule").click(function() {

    $.ajax({
        "url": $(this).attr("href"),
        "success": function(data) {
            $(".manager_body").html(data);
            $(".day_schedule_delete").click(enable_week_schedule_delete);
            $(".schedule_add").click(get_week_day_schedule_form);

            $(".week_day").click(function(){
                $(".week_day").removeClass('active');
                $(this).addClass('active');
                
                let index = $(this).attr("index");
                $(".revert").attr("href", `/revert_week_day/${index}/`);
            
                $.ajax({
                    "url": $(this).attr("href"),
                    "success": function(data) {
                        
                        let reverter = $(".revert");
                        $(reverter).attr("revert", index);

                        $(".day_schedules").html(data);
                        $(".day_schedules").append(reverter);

                        $(".revert").click(enable_reverter);
                        
                        $(".day_schedule_delete").click(enable_week_schedule_delete);
                        
                        $(".schedule_add").click(get_week_day_schedule_form);
                    }
                });
            });      
            
            $(".revert").click(enable_reverter);
        }
    });
});

$("button#schedule_applier").click(function() {
    $.ajax({
        "url": $(this).attr("href"),
        "success": function(data) {
            $(".manager_body").html(data);
            $(".apply_schedule").submit(function(e) {
                e.preventDefault();

                $.ajax({
                    "url": $(this).attr("action"),
                    "type": "GET",
                    "data": $(this).serialize(),
                    "success": function(data) {
                        try {
                            data = JSON.parse(data);
                        }
                        catch (err) {
                            console.log("invalid log !!!");
                        }

                        if (data["status"]) {
                            $(".message_box").html(data["message"]);
                        }
                        else {
                            alert("Couldn't apply the schedules !!!");
                        }
                    }
                });
            });
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