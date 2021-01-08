// Default root ID always 1
ROOT_QUESTION_ID = "1"
if (localStorage.getItem("questionID") === null){
    localStorage.setItem("questionID", ROOT_QUESTION_ID);
    localStorage.setItem("pastQNA", "[]");
}

$.ajax({
    url: "questions",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({
        "questionID":localStorage.getItem("questionID")
    }),
    success: function (data) {
        localStorage.setItem("questionID", data["questionID"]);
        updateQuestions(data);
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
    var questionID = localStorage.getItem("questionID");
    var answerID = $("#answers input[name=choice]:checked").val();
    if (answerID !== "" && answerID !== undefined && answerID !== null) {
        $.ajax({
            url: "next",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                "questionID": questionID,
                "answerID": answerID
            }),
            success: function (data) {
                // add past question and answer to the stack
                let pastQNA = JSON.parse(localStorage.getItem("pastQNA"));
                pastQNA.unshift({"questionID": questionID, "answerID": answerID});
                localStorage.setItem("pastQNA", JSON.stringify(pastQNA));

                // point current page to the new id
                localStorage.setItem("questionID", data["questionID"]);
                updateQuestions(data);
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
 * going to the previous option
 */
$("#prev").on("click", function () {
    // look at the stack top to see what's the preivous question ID
    let pastQNA = JSON.parse(localStorage.getItem("pastQNA"));
    var prevQuestionID = pastQNA[0]["questionID"];
    $.ajax({
        url: "prev",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            "prevQuestionID": prevQuestionID
        }),
        success: function (data) {
            // pop the fisrt item in stack
            pastQNA.shift();
            localStorage.set("pastQNA", JSON.stringify(pastQNA));

            // update the current page id
            localStorage.setItem("questionID", data["questionID"]);
            updateQuestions(data);
        },
        error: function (jqXHR, exception) {
             // TODO add error handling
            $("#error").find(".modal-body").empty().append(jqXHR.responseText);
            $("#error").modal("show");
        }
    });
});

// /**
//  * submit the final result and generate a checklist of resources
//  */
// $("#submit").on("click", function () {
//     var submittedNid = localStorage.getItem("questionID");
//     if (submittedNid !== "" && submittedNid !== undefined && submittedNid !== null) {
//         $.ajax({
//             url: "submit",
//             type: "POST",
//             contentType: "application/json",
//             data: JSON.stringify({
//                 "submitted_nid": submittedNid
//             }),
//             success: function (data) {
//                 $("#survey-title").empty();
//                 $("#survey-description").empty();
//                 $("#answers").empty();
//
//                 // hide all buttons except restart
//                 $("#prev").hide();
//                 $("#next").hide();
//                 $("#submit").hide();
//
//                 // show download zip button
//                 $("#download-zip").show();
//
//                 // update resource list
//                 $("#resource-list").empty();
//                 data.past_nodes.forEach(function(pastNode, i) {
//                     var element = $(`<div class="resource">
//                                         <h2>` + pastNode["tag"] + `</h2><p>` + pastNode.data["explanation"] + `</p>
//                                         <ul class="resource-file-list"></ul></div>`);
//                     pastNode.data["file_list"].forEach(function(filename, j){
//                         var fileURL = "/download/".concat(filename);
//                         element.find(".resource-file-list").append(`<li><a href="` + fileURL + `" target="_blank">`
//                             + filename + `</a></li>`);
//                     });
//                     $("#resource-list").append(element);
//                 });
//             },
//             error: function (jqXHR, exception) {
//                  // TODO add error handling
//                 $("#error").find(".modal-body").empty().append(jqXHR.responseText);
//                 $("#error").modal("show");
//             }
//         });
//     } else {
//         alert("You did not identify what node id to submit!");
//     }
// });


/**
 * jump to the root and restart the survey questions
 */
$("#restart").on("click", function () {
    localStorage.setItem("questionID", ROOT_QUESTION_ID);
    $.ajax({
        url: "questions",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            "questionID":localStorage.getItem("questionID")
        }),
        success: function (data) {
            updateQuestions(data);
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
 * update questions page with new data
 * @param data
 */
function updateQuestions(data){
    // hide download button
    $("#download-zip").hide();

    // if it's the root node hide prev button
    if (data["questionID"] === ROOT_QUESTION_ID){
        $("#prev").hide();
    }
    else{
        $("#prev").show();
    }

    $("#question-title").empty().append(data["question"]);
    $("#question-description").empty().append(data["description"])
    $("#answers").empty();
    data["answers"].forEach(function(option, index){
        $("#answers").append(
        `<div class="answer"><input type="radio" name="choice" value="` + option["answerID"]+ `">
         <label>` + option["answer"] + `</label>
         <p>` + option["description"] + `</p>
         </div>`
        );
    });
    $("#question-resource-list").empty();
    $("#answer-resource-list").empty();

}