function snackbar(succes, snackbarid, id) {

    if (succes == false) {
        let snackbar = document.getElementById(snackbarid);
        snackbar.classList.add("show");
        setTimeout(function(){ snackbar.className = snackbar.className.replace("show", ""); }, 6000);
        document.getElementById(id).className = "form-control is-invalid";
    }
}


function pass_check() {
    document.getElementById("password").className = "form-control";
    document.getElementById("confirmation").className = "form-control";
    var password = document.getElementById("password").value;
    var confirmation = document.getElementById("confirmation").value;

    numbers = /\d/.test(password);

    if (password.length >= 6 && password.length < 20 && numbers && password.indexOf(" ") == -1) {
        if (password == confirmation) {
            correctness = [true, true];
        }
        else {
        correctness = [true, false];
        }
    }
    else if (password == confirmation) {
        correctness = [false, true];
    }
    else {
    correctness = [false, false];
    }

    snackbar(correctness[0], "passwordsnackbar", "password");
    snackbar(correctness[1], "confirmsnackbar", "confirmation");

    return correctness;
}


function user_check() {
    document.getElementById("username").className = "form-control";
    var username = document.getElementById("username");
    var user = $.get("/check_username?username=" + username.value);
    return user;
}


function register_check() {
    user_check().done(function(user){
        var pass = pass_check();
        var my_form = document.querySelector("form");

        snackbar(user, "usersnackbar", "username");

        if (user == false || pass[0] == false || pass[1] == false) {
            my_form.reset();
        }
        else {
            my_form.submit();
        }
    });
}

function login_check() {
    document.getElementById("password").className = "form-control";
    document.getElementById("username").className = "form-control";
    var password = document.getElementById("password").value;
    var username = document.getElementById("username").value;

    $.post("/check_login", {username: username, password: password}, function(data) {
        var my_form = document.querySelector("form");
        snackbar(data, "loginsnackbar", "username", false);

        if (data == false) {
            document.getElementById("password").className = "form-control is-invalid";
            my_form.reset();
        }
        else {
            my_form.submit();
        }
    });
}
