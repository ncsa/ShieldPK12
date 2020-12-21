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
        updateQuestions(data.current_node, data.option_nodes, data.root_nid);
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
    if (selectedNid !== "" && selectedNid !== undefined && selectedNid !== null) {
        $.ajax({
            url: "next",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                "selected_nid": selectedNid
            }),
            success: function (data) {
                localStorage.setItem("current_nid", data.current_node["_identifier"]);
                updateQuestions(data.current_node, data.option_nodes, data.root_nid);
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
 * submit the final result and generate a checklist of resources
 */
$("#submit").on("click", function () {
    var submittedNid = localStorage.getItem("current_nid");
    if (submittedNid !== "" && submittedNid !== undefined && submittedNid !== null) {
        $.ajax({
            url: "submit",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                "submitted_nid": submittedNid
            }),
            success: function (data) {
                data.past_nodes.forEach(function(pastNode, index) {
                    $("#resource-list").append(`
                        <div class="resource">
                            <p>(` + pastNode["_tag"] + `)</p>
                            <button>Download</button>
                            <a href="">Read More...</a>
                        </div>
                    `);
                });
            },
            error: function (jqXHR, exception) {
                 // TODO add error handling
                $("#error").find(".modal-body").empty().append(jqXHR.responseText);
                $("#error").modal("show");
            }
        });
    } else {
        alert("You did not identify what node id to submit!");
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
            updateQuestions(data.current_node, data.option_nodes, data.root_nid);
        },
        error: function (jqXHR, exception) {
            // TODO add error handling
            $("#error").find(".modal-body").empty().append(jqXHR.responseText);
            $("#error").modal("show");
        }
    });
});

function updateQuestions(current_node, option_nodes, root_nid=1){
    // if it's the root node hide prev button
    if (current_node["_identifier"] === root_nid){
        $("#prev").hide();
    }
    else{
        $("#prev").show();
    }

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
    $("#resource-list").empty();
    option_nodes.forEach(function(option, index){
        $("#survey-options").append(
        `<input type="radio" name="choice" value="` + option["_identifier"]+ `"> ` + option["_tag"]
        );
    });
}