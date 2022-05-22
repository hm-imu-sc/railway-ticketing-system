let password_field = $("#password");
let retype_password_field = $("#retype_password");

function password_verify() {
    let password = $(password_field).val();
    let retype_password = $(retype_password_field).val();

    if (password == retype_password && password.length >= 6 && password.length <= 20) {
        $("input[type='submit']").addClass("enabled");
        $("input[type='submit']").removeClass("disabled");
        $("input[type='submit']").prop('disabled', false);
    }
    else {
        $("input[type='submit']").removeClass("enabled");
        $("input[type='submit']").addClass("disabled");
        $("input[type='submit']").prop('disabled', true);
    }
}

$(password_field).keyup(password_verify);
$(retype_password_field).keyup(password_verify);