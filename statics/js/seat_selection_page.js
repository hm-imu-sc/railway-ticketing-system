$("#number_of_seats").change(function(){
    $("span.number_of_seats").text($(this).val());
});

$("button.check").click(function(){
    let number_of_seats = Number.parseInt($("#number_of_seats").val());
    let car = Number.parseInt($("#car_id").val()) - 1;

    if (car == -1) {
        return;
    }

    let car_types = ['FCB', 'FCS', "SC", "S"];

    $("#seats").text('');

    for (let i=6; i<number_of_seats+6; i++) {
        if (i!=6) {
            $("#seats").append(", ");
        }
        $("#seats").append(""+car_types[car]+"-"+i);
    }
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