$.ajax({
    url: "questions",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({
        "current_nid":localStorage.getItem("current_nid")
    }),
    success: function (data) {
        // store current id to session storage
        if (localStorage.getItem("root_nid") === null){
            localStorage.setItem("root_nid", data.root_nid);
        }
        localStorage.setItem("current_nid", data.current_node["_identifier"]);
        updateQuestions(data.current_node, data.option_nodes);
    },
    error: function (jqXHR, exception) {
        // TODO add error handling
        $("#error").find(".modal-body").empty().append(jqXHR.responseText);
        $("#error").modal("show");
    }
});

/**
 * submit the selection and go to next step
 */
$("#next").on("click", function () {
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
                localStorage.setItem("current_nid", data.current_node["_identifier"]);
                updateQuestions(data.current_node, data.option_nodes);
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

/**
 * going to the last option
 */
$("#prev").on("click", function () {
    var currentNid = localStorage.getItem("current_nid");
    $.ajax({
        url: "prev",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            "current_nid": currentNid
        }),
        success: function (data) {
            localStorage.setItem("current_nid", data.current_node["_identifier"]);
            updateQuestions(data.current_node, data.option_nodes);
        },
        error: function (jqXHR, exception) {
             // TODO add error handling
            $("#error").find(".modal-body").empty().append(jqXHR.responseText);
            $("#error").modal("show");
        }
    });
});

/**
 * jump to the root and restart the survey questions
 */
$("#restart").on("click", function () {
    var rootNid = localStorage.getItem("root_nid");
    localStorage.setItem("current_nid", rootNid);
    $.ajax({
        url: "questions",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            "current_nid":localStorage.getItem("current_nid")
        }),
        success: function (data) {
            localStorage.setItem("current_nid", data.current_node["_identifier"]);
            updateQuestions(data.current_node, data.option_nodes);
        },
        error: function (jqXHR, exception) {
            // TODO add error handling
            $("#error").find(".modal-body").empty().append(jqXHR.responseText);
            $("#error").modal("show");
        }
    });
});

function updateQuestions(current_node, option_nodes){
    // if no options meaning reach the end of the node
    if (option_nodes.length === 0) {
        $("#next").hide();
        $("#submit").show();
    }
    else{
         $("#next").show();
         $("#submit").hide();
    }

    $("#survey-title").empty().append(current_node["_tag"] + "?");
    $("#survey-options").empty();
    option_nodes.forEach(function(option, index){
        $("#survey-options").append(
        `<input type="radio" name="choice" value="` + option["_identifier"]+ `"> ` + option["_tag"]
        );
    });
}