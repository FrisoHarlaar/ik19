function new_question(input) {
    // when page loads
    if (input == 'setup') {
        $("#transition").addClass('transition_block');
    }

    // when button is clicked
    else {
        $("#transition").addClass('transition_block_away');
    }

    // send post request to server
    $.post("/triviagame", {answer: input}, function(data) {
        // reset timer
        window.clearTimeout(time);
        timer(data.duration);

        // reset timer bar
        document.getElementById("bar").innerHTML = "";

        // if page is first loaded
        if (data.load == true) {

            // animate timer bar
            circle = new ProgressBar.Circle('#bar', {
                color: "#fecb4c",
                strokeWidth: 6,
                duration: data.duration + 2000,
                easing: 'easeInOut'
            });
            circle.animate(1);
        }

        // if user is out of lives
        else if (data == false) {

            // end timer and redirect to game over
            window.clearTimeout(time);
            window.location.href = "/game_over";
        }
        else {

            // update question, score and answers
            document.getElementById("score").innerHTML = data.score;
            document.getElementById("question").innerHTML = data.question;
            document.getElementById("answers").innerHTML = "";
            let i;
            for (i = 0; i < data.answers.length; i++) {
                document.getElementById("answers").innerHTML += "<button type='submit' name='answer' value='" + data.answers[i] + "' class='btn answer'>" + data.answers[i] + "</button>";
            }

            // question and answers fade in animation
            $("#transition").removeClass('transition_block_away').addClass('transition_block');

            // get right amount of broken hearts
            for (i = 0; i < (4 - data.lives); i++) {
                $("#heart" + i).attr("src", "static/images/broken_hearth.png").attr("alt", "broken_hearth");
                $("#heart" + i).addClass('fadein');
            }

            // if score reaches table of ten and lives is less then 5 add extra heart
            if (data.score % 10 == 0) {
                if (data.lives < 5) {
                    $("#heart" + (4 - data.lives)).removeClass("hearth").addClass("fadein hearth");
                    $("#heart" + (4 - data.lives)).attr("src", "static/images/hearth.png").attr("alt", "hearth");
                }
            }

            // animate timer bar
            circle = new ProgressBar.Circle('#bar', {
                color: "#fecb4c",
                strokeWidth: 6,
                duration: data.duration + 2000,
                easing: 'easeInOut'
            });
            circle.animate(1);
        }
    });
}

// timer function
var time;
function timer(duration) {
    time = window.setTimeout(function() {

        // when time is up get new question and reset timer
        new_question("Tijd is om");
        timer(duration);
    }, duration);
}