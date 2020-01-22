function pass_check() {
    document.getElementById("password").className = "form-control";
    document.getElementById("confirmation").className = "form-control";
    var password = document.getElementById("password").value;
    var confirmation = document.getElementById("confirmation").value;
    var my_form = document.querySelector("form");

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

    if (correctness[0] == false) {
        let snackbar = document.getElementById("passwordsnackbar");
        snackbar.classList.add("show");
        setTimeout(function(){ snackbar.className = snackbar.className.replace("show", ""); }, 6000);
        document.getElementById("password").className = "form-control is-invalid";
    }
    if (correctness[1] == false) {
        let snackbar = document.getElementById("confirmsnackbar");
        snackbar.classList.add("show");
        setTimeout(function(){ snackbar.className = snackbar.className.replace("show", ""); }, 6000);
        document.getElementById("confirmation").className = "form-control is-invalid";
    }
    return correctness;
}


function user_check(callback) {
    document.getElementById("username").className = "form-control";
    var my_form = document.querySelector("form");
    var username = document.getElementById("username");
    var user = $.get("/check_username?username=" + username.value, function(available) {
        var availability = $.parseJSON(available);
        if (availability == false) {
            let snackbar = document.getElementById("usersnackbar");
            snackbar.classList.add("show");
            setTimeout(function(){ snackbar.className = snackbar.className.replace("show", ""); }, 6000);
            document.getElementById("username").className = "form-control is-invalid";
        }
    });
    return user;
}


function register_check() {
    user_check().done(function(user){
        var pass = pass_check();
        var my_form = document.querySelector("form");

        if (user == false || pass[0] == false || pass[1] == false) {
            my_form.reset();
        }
        else {
            my_form.submit();
        }
    });
}
