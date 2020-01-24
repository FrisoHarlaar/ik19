function snackbar(status, snackbarid, id, value) {

    /* show error-snackbar if status is false */
    if (status == value) {
        let snackbar = document.getElementById(snackbarid);
        snackbar.classList.add("show");
        setTimeout(function(){ snackbar.className = snackbar.className.replace("show", ""); }, 6000);
        document.getElementById(id).className = "form-control is-invalid";
    }
}


function pass_check(id, id2) {
    /* reset input boxes when form is submitted */
    document.getElementById(id).className = "form-control";
    document.getElementById(id2).className = "form-control";

    /* get user input from form */
    var password = document.getElementById(id).value;
    var confirmation = document.getElementById(id2).value;

    /* check if password contains number */
    numbers = /\d/.test(password);
    console.log([password, confirmation]);
    /* check if password meets the requirements */
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

    return correctness;
}


function user_check(id) {
    document.getElementById(id).className = "form-control";
    var username = document.getElementById(id);
    var user = $.get("/check_username?username=" + username.value);

    return user;
}

function change_user() {
    user_check("newusername").done(function(user) {

        /* get form */
        var my_form = document.querySelector("form");

        /* show snackbar-error if username is taken */
        snackbar(user, "loginsnackbar", "newusername", false);

        /* if username is free submit else reset form */
        if (user == false) {
            my_form.submit();
        }
        else {
            my_form.reset();
        }
    });
}

function add_friend() {
    user_check("friendname").done(function(user) {

        /* get form */
        var my_form = document.querySelector("form");

        /* show snackbar-error if username is taken */
        snackbar(user, "loginsnackbar", "friendname", true);

        /* if friend exists and is not empty submit else reset form */
        var friend = document.getElementById("friendname").value;
        console.log([user, friend]);
        if (friend.length < 1) {
            snackbar(false, "loginsnackbar", "friendname", false);
            my_form.reset();
        }
        else if (user == false) {
            $.post("/check_friend", {friendname:friend}, function(check) {
                var my_form = document.querySelector("form");

                if (check == true) {
                    my_form.submit();
                }
                else {
                    snackbar(false, "friendsnackbar", "friendname", false);
                    my_form.reset();
                }
            });
        }
        else {
            my_form.reset();
        }
    });
}

function register_check() {

    /* work with data from async user_check */
    user_check("username").done(function(user){
        var pass = pass_check("password", "confirmation");

        /* show error snackbars */
        snackbar(pass[0], "passwordsnackbar", "password", false);
        snackbar(pass[1], "confirmsnackbar", "confirmation", false);
        snackbar(user, "usersnackbar", "username", false);

        /* get form */
        var my_form = document.querySelector("form");

        /* reset form if any of the checks return false */
        if (user == false || pass[0] == false || pass[1] == false) {
            my_form.reset();
        }
        else {
            my_form.submit();
        }
    });
}


function login_check() {

    /* reset input boxes when form is submitted */
    document.getElementById("password").className = "form-control";
    document.getElementById("username").className = "form-control";

    /* get user input from form */
    var password = document.getElementById("password").value;
    var username = document.getElementById("username").value;

    /* send user input to application.py */
    $.post("/check_login", {username: username, password: password}, function(user) {

        /* get form */
        var my_form = document.querySelector("form");

        /* reset form and show error if user input is false */
        if (user == false) {
            snackbar(user, "loginsnackbar", "username", false);
            document.getElementById("password").className = "form-control is-invalid";
            my_form.reset();
        }
        else {
            my_form.submit();
        }
    });
}

function change_pass() {
    /* reset input boxes when form is submitted */
    document.getElementById("oldpassword").className = "form-control";
    document.getElementById("newpassword").className = "form-control";
    document.getElementById("confirmation").className = "form-control";

    /* get user input */
    var old_password = document.getElementById("oldpassword").value;
    var new_password = document.getElementById("newpassword").value;
    var confirmation = document.getElementById("confirmation").value;

    /* error if confirmation isn't equal to password */
    snackbar((confirmation == new_password), "confirmsnackbar", "confirmation");

    /* error if password field is empty */
    snackbar((old_password != ""), "emptysnackbar", "oldpassword");

    /* error if old and new password are equal */
    if (old_password == new_password) {
        snackbar(false, "samesnackbar", "oldpassword", false);
        my_form.reset();
    }
    else {
        /* check if old password is correct */
        $.post("/check_changepass", {oldpassword: old_password}, function(status) {

            /* check if new password meets requirements */
            var pass = pass_check("newpassword", "confirmation");

            snackbar(pass[0], "changesnackbar", "newpassword", false);
            snackbar(pass[1], "confirmsnackbar", "confirmation", false);
            snackbar(status, "oldsnackbar", "oldpassword", false);

            /* get form */
            var my_form = document.querySelector("form");

            /* submit form if all checks return true */
            if (status == true && pass[0] == true && pass[1] == true) {
                my_form.submit();
            }
            else {
                my_form.reset();
            }
        });
    }
}