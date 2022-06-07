
let seats = -1;
let fare = -1;

$("#number_of_seats").change(function(){
    $("span.number_of_seats").text($(this).val());
});

$("button.check").click(function(){
    if ($("#car_type").val() === "-1") {
        return;
    }

    let number_of_seats = Number.parseInt($("#number_of_seats").val());
    let url = $("#car_type").val().split("-")[0]+number_of_seats+"/";

    let params = url.split("/")

    $("#pay").attr("href", `/seat_purchase/${params[2]}/${params[3]}/${params[4]}/`);

    $.ajax({
        "url": url,
        "success": function(data) {
            try {
                data = JSON.parse(data);
            }
            catch (err) {
                console.log(err.message);
            }

            if (data["status"]) {
                seats = data["seats"];
                fare = data["fare"];
                car = data["car"];

                let car_types = ['FCB', 'FCS', "SC", "S"];

                $("#seats").text('');
            
                for (let i=seats; i<seats+number_of_seats; i++) {
                    if (i!=seats) {
                        $("#seats").append(", ");
                    }
                    $("#seats").append(""+car_types[car]+"-"+i);
                }
            }
            else {
                $("#seats").html(data["message"]);
            }
        } 
    });
});

$("button.purchase").click(function() {
    if (seats == -1) {
        return;
    } 

    let number_of_seats = Number.parseInt($("#number_of_seats").val());
    let car = $("#car_id").val();

    $("span.bill").html("" + number_of_seats*fare + " BDT.");
    $(".bill_info").css("display", "flex");
});

$("#pay").click(function(){
    let url = $(this).attr("href");
    $.ajax({
        "url": url,
        "success": function(data) {
            try {
                data = JSON.parse(data);
            }
            catch (err) {   
                console.log(err.message);
            }

            if (data["status"]) {
                alert(data["message"]);
                window.location.href = window.location.href;
            }
            else {
                alert("Error purchasing tickets !!!");
            }
        }
    });
});