$.ajax({
    url: "questions",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({
        "current_nid":sessionStorage.getItem("current_nid")
    }),
    success: function (data) {
        // store current id to session storage
        sessionStorage.setItem("current_nid", data.current_nid);

        // update the questionaire
        updateQuestions(data.option_nodes);
    },
    error: function (jqXHR, exception) {
        // TODO add error handling
        $("#error").find(".modal-body").empty().append(jqXHR.responseText);
        $("#error").modal("show");
    }
});


function updateQuestions(option_nodes){
    $("#survey-options").empty();
    option_nodes.forEach(function(option, index){
        $("#survey-options").append(
        `<input type="radio" name="choice" value="` + option["_identifier"]+ `"> ` + option["_tag"]
        );
    });
}

$("#next button").on("click", function () {
    var selectedNid = $("#survey-options input[name=choice]:checked").val();
    if (selectedNid !== "" && selectedNid !== undefined) {
        $.ajax({
            url: "next",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                "selected_nid": selectedNid
            }),
            success: function (data) {
                // store current id to session storage
                sessionStorage.setItem("current_nid", data.current_nid);

                // update the questionaire
                updateQuestions(data.option_nodes);
            },
            error: function (jqXHR, exception) {
                 // TODO add error handling
                $("#error").find(".modal-body").empty().append(jqXHR.responseText);
                $("#error").modal("show");
            }
        });
    } else {
        alert("You have to select an option!");
    }
});

$("#prev button").on("click", function () {
    var currentNid = sessionStorage.getItem("current_nid");
    $.ajax({
        url: "prev",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            "current_nid": currentNid
        }),
        success: function (data) {
            // store current id to session storage
            sessionStorage.setItem("current_nid", data.current_nid);

            // update the questionaire
            updateQuestions(data.option_nodes);
        },
        error: function (jqXHR, exception) {
             // TODO add error handling
            $("#error").find(".modal-body").empty().append(jqXHR.responseText);
            $("#error").modal("show");
        }
    });
});