$(".download").click(function(){
    $(".navbar, h1, .download").css("display", "none");
    print();
    $("h1, .download").css("display", "block");
    $(".navbar").css("display", "flex");
});