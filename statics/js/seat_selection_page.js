
let seats = [];

$("#number_of_seats").change(function(){
    $("span.number_of_seats").text($(this).val());
});

$("button.check").click(function(){
    let number_of_seats = Number.parseInt($("#number_of_seats").val());
    let url = $("#car_type").val().split("-")[0]+number_of_seats+"/";

    $.ajax({
        "url": url,
        "success": function(data) {
            try {
                data = JSON.parse(data);
            }
            catch (err) {
                console.log(err.message);
            }

            seats = data["seats"];
        } 
    });
});

$("button.purchase").click(function() {
    let number_of_seats = Number.parseInt($("#number_of_seats").val());
    let car = Number.parseInt($("#car_id").val()) ;

    if (car == 0) {
        return;
    }

    let car_types = [1500, 1250, 750, 500];

    $("span.bill").append("" + number_of_seats*car_types[car] + " BDT.");
    $(".bill_info").css("display", "flex");
});

$("#pay").click(function(){
    alert("Payment successfull !!!");
});