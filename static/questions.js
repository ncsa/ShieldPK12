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
        localStorage.setItem("current_nid", data.current_node["identifier"]);
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
                localStorage.setItem("current_nid", data.current_node["identifier"]);
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
                $("#survey-title").empty();
                $("#survey-description").empty();
                $("#survey-options").empty();

                // hide all buttons except restart
                $("#prev").hide();
                $("#next").hide();
                $("#submit").hide();

                // update resource list
                $("#resource-list").empty();
                data.past_nodes.forEach(function(pastNode, i) {
                    var element = $(`<div class="resource">
                                        <h2>` + pastNode["tag"] + `</h2><p>` + pastNode.data["explanation"] + `</p>
                                        <ul class="resource-file-list"></ul></div>`);
                    pastNode.data["file_list"].forEach(function(filename, j){
                        var fileURL = "/download/".concat(filename);
                        element.find(".resource-file-list").append(`<li><a href="` + fileURL + `" target="_blank">`
                            + filename + `</a></li>`);
                    });
                    $("#resource-list").append(element);
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
            localStorage.setItem("current_nid", data.current_node["identifier"]);
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
            localStorage.setItem("current_nid", data.current_node["identifier"]);
            updateQuestions(data.current_node, data.option_nodes, data.root_nid);
        },
        error: function (jqXHR, exception) {
            // TODO add error handling
            $("#error").find(".modal-body").empty().append(jqXHR.responseText);
            $("#error").modal("show");
        }
    });
});

/**
 * download complete resources in a zipfile
 */
$("#download-zip").on("click", function(){
    // gathering the filename from the current page
    var filenameList = [];
    var aTagArray = $(".resource-file-list").find("a").toArray();
    for (var i=0; i<aTagArray.length; i++) {
        filenameList.push(aTagArray[i].text);
    }
     $.ajax({
        url: "download-zip",
        type: "POST",
        contentType: "application/json",
        xhrFields:{
            responseType: "blob"
        },
        data: JSON.stringify({
            "filename_list":filenameList
        }),
        success: function (data) {
            var downloadUrl = window.URL.createObjectURL(data);
            // TODO: might be different name or multiple names
            var filename = "resources.zip";
            // use HTML5 a[download] attribute to specify filename
            var a = document.createElement("a");
            // safari doesn't support this yet
            if (typeof a.download === 'undefined') {
                window.location.href = downloadUrl;
            } else {
                a.href = downloadUrl;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
            }

            setTimeout(function () { window.URL.revokeObjectURL(downloadUrl); }, 100); // cleanup
        },
        error: function (jqXHR, exception) {
            // TODO add error handling
            $("#error").find(".modal-body").empty().append(jqXHR.responseText);
            $("#error").modal("show");
        }
    });
});

/**
 *
 * @param current_node
 * @param option_nodes
 * @param root_nid
 */
function updateQuestions(current_node, option_nodes, root_nid=1){
    // if it's the root node hide prev button
    if (current_node["identifier"] === root_nid){
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

    $("#survey-title").empty().append(current_node["tag"] + "?");
    $("#survey-description").empty().append(current_node["data"]["explanation"])
    $("#survey-options").empty();
    $("#resource-list").empty();
    option_nodes.forEach(function(option, index){
        $("#survey-options").append(
        `<div class="survey-option"><input type="radio" name="choice" value="` + option["identifier"]+ `">
         <label>` + option["tag"] + `</label></div>`
        );
    });
}