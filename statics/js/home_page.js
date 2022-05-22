
let current_week = 0;

function get_schedule() {
    let source = $("#depart_from").val();
    let destination = $("#destination").val();
    let date = $('#' + $('label.active').attr('for')).val();

    $.ajax({
        'url': '/get_schedule/' + date + "/" + source + "/" + destination,
        'success': data => {
            console.log(data);
            $('.train_list').html(data);
        }
    });
}

$("input[name='date']").click(function(){
    $(".date_part label").removeClass("active");
    $("label[for='" + $(this).attr("id") + "']").addClass("active");

    get_schedule();
});

$("#depart_from").change(get_schedule);
$("#destination").change(get_schedule);

$("#prev_week").click(function(){
    if (current_week > 0) {
        current_week--;
        
        $(".day_date").addClass("week_hidden");
        $(".week_" + current_week).removeClass("week_hidden");

        if (current_week == 0) {
            $("#week_info").text("Current Week");
        }
        else {
            $("#week_info").text(current_week + " Week Later");
        }
    }
});

$("#next_week").click(function(){
    if (current_week < 2) {
        current_week++;
        
        $(".day_date").addClass("week_hidden");
        $(".week_" + current_week).removeClass("week_hidden");

        $("#week_info").text(current_week + " Week Later");
    }
});