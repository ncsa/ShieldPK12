// Default root ID always 1
ROOT_QUESTION_ID = "1"

// GET current module
// assume pattern will be /module/questions
var module = $(location).attr('href').split("/").slice(-2)[0];
$("#module-name").empty().text(module);

if (localStorage.getItem("QID") === null
    || localStorage.getItem("module") === null
    || localStorage.getItem("pastQNA") === null
    || localStorage.getItem("module") !== module
){
    // intialized
    localStorage.setItem("module", module);
    localStorage.setItem("QID", ROOT_QUESTION_ID);
    localStorage.setItem("pastQNA", "[]");
}

/**
 * update page when document ready
 */
$(document).ready(function () {
    $.ajax({
        url: "questions",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            "QID": localStorage.getItem("QID"),
            "qna": JSON.parse(localStorage.getItem("pastQNA"))
        }),
        success: function (data) {
            if ("page" in data) {
                localStorage.setItem("QID", data.page["QID"]);
            var answerNumQ = JSON.parse(localStorage.getItem("pastQNA")).length;
            updateQuestions(data, answerNumQ);
            } else if ("report" in data && "checklist" in data) {
                localStorage.setItem("QID", null);
                updateResult(data);
            }
        },
        error: function (jqXHR, exception) {
            $("#error").find("#error-message").empty().append(jqXHR.responseText);
            $("#error").modal("show");
        }
    });
})


/**
 * submit the selection and go to next step
 */
$("#next").on("click", function () {
    var QID = localStorage.getItem("QID");
    var AID = [];

    if ($("#answers").attr("multiple-answers") === "true") {
         $("#answers input[type='checkbox']").each(function () {
            if (this.checked) {
                AID.push($(this).val());
            }
        });
    }
    else {
        var checked = $("#answers input[type='radio']:checked").val();
        if (checked !== undefined) AID = [checked];
    }

    if (AID !== undefined && AID !== null && AID.length > 0) {
        $.ajax({
            url: "next",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                "QID": QID,
                "AID": AID,
                "qna": JSON.parse(localStorage.getItem("pastQNA"))
            }),
            success: function (data) {
                // add past question and answer to the stack
                let pastQNA = JSON.parse(localStorage.getItem("pastQNA"));
                updatedPastQNA = addQNAtoHistory(QID, AID, pastQNA)
                localStorage.setItem("pastQNA", JSON.stringify(updatedPastQNA));

                if ("page" in data) {
                    localStorage.setItem("QID", data.page["QID"]);
                    updateQuestions(data, pastQNA.length);
                } else if ("report" in data && "checklist" in data) {
                    localStorage.setItem("QID", null);
                    updateResult(data);
                }
            },
            error: function (jqXHR, exception) {
                $("#error").find("#error-message").empty().append(jqXHR.responseText);
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
    var prevQID = pastQNA[0]["QID"];
    $.ajax({
        url: "prev",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            "prevQID": prevQID
        }),
        success: function (data) {
            // pop the fisrt item in stack
            pastQNA.shift();
            localStorage.setItem("pastQNA", JSON.stringify(pastQNA));

            // update the current page id
            localStorage.setItem("QID", data.page["QID"]);
            updateQuestions(data, pastQNA.length);
        },
        error: function (jqXHR, exception) {
            $("#error").find("#error-message").empty().append(jqXHR.responseText);
            $("#error").modal("show");
        }
    });
});


/**
 * jump to the root and restart the survey questions, clear all past histories
 */
$("#restart").on("click", function () {
    localStorage.setItem("QID", ROOT_QUESTION_ID);
    localStorage.setItem("pastQNA", "[]");
    $.ajax({
        url: "questions",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            "QID":localStorage.getItem("QID"),
            "qna":[]
        }),
        success: function (data) {
            updateQuestions(data, JSON.parse(localStorage.getItem("pastQNA")).length);
        },
        error: function (jqXHR, exception) {
            $("#error").find("#error-message").empty().append(jqXHR.responseText);
            $("#error").modal("show");
        }
    });
});


/**
 * generate pdf for the report page
 */
$("#download-pdf").on("click", function () {
    html2pdf()
        .set({
            margin: 1,
            pagebreak: {mode: ['avoid-all', 'css', 'legacy']},
            filename: "my-playbook-report.pdf",
            jsPDF: {unit: 'in', format: 'letter', orientation: 'portrait'}
        })
        .from(document.getElementById("result-pdf"))
        .save();
})

/**
 * update questions container including question and answer
 * @param data
 * @param answeredNumQ
 */
function updateQuestions(data, answeredNumQ) {
    $("#result-container").hide();
    $("#qna-container").show();

    // if it's the root node hide prev button
    if (data.page["QID"] === ROOT_QUESTION_ID) {
        $("#prev").hide();
    } else {
        $("#prev").show();
    }

    // enable next
    $("#next").show();

    // update progress bar
    updateProgressBar(data.minNumQ, answeredNumQ)

    // for questions
    var questionTitle = data.page["QID"] + ". " + data.page["question"]
    $("#question-title").text(questionTitle);
    if ("multiple" in data.page && data.page["multiple"] === true){
        $("#question-subtitle").text("(select all that applies)");
    }
    else{
        $("#question-subtitle").text("");
    }
    $("#question-description").text(data.page["description"]);

    // for answers
    $("#answers").removeAttr("multiple-answers").empty();
    data.page["answers"].forEach(function(option, index){
        // do not display empty question
        if (option["answer"] !== ""){
            if ("multiple" in data.page && data.page["multiple"] === true) {
                $("#answers").attr("multiple-answers", true).append(
                    `<div class="answer"><input type="checkbox" name="choice" value="` + option["AID"] + `">
                <h2 class="answer-text"><span class="answer-pretty-id">` + option["prettyAID"] +
                    `</span>` + option["answer"] + `</h2>
                <p class="answer-description">` + option["description"] + `</p>
                </div>`);
            } else {
                $("#answers").attr("multiple-answers", false).append(
                    `<div class="answer">
                <input type="radio" name="choice" value="` + option["AID"] + `">
                <h2 class="answer-text"><span class="answer-pretty-id">` + option["prettyAID"] + `</span>`
                    + option["answer"] + `</h2>
                <p class="answer-description">` + option["description"] + `</p>
            </div>`);
            }
        }
        else{
             $("#answers").attr("multiple-answers", false).append(`<div class="answer" style="display:none;">
                <input type="radio" name="choice" value="` + option["AID"]+ `" hidden checked></div>`);
        }
    });

    // TODO add question resource list and answer resource list
    $("#question-resource-list").empty();
    $("#answer-resource-list").empty();
}


/**
 * update results container including checklist and report
 * @param data
 */
function updateResult(data) {
    $("#result-container").show();
    $("#qna-container").hide();

    // hide next
    $("#next").hide();

    // update status bar
    updateProgressBar(1, 1);
    generateChecklist(data.checklist);
    generateReport(data.report);
}

/**
 * generate checklist
 * @param checklist
 */
function generateChecklist(checklist) {
    $(".checklists").empty();
    checklist.forEach(function (item, index) {
        $(".checklists").append(`
            <div class="checklist">
                <a class="checklist-activity" href="#" target="_blank">` + item["activity"] + `</a>
            </div>
        `);
    });
}

/**
 *
 * @param report
 */
function generateReport(report){
    $(".report-container").empty();
    report.forEach(function (item, index) {
        $(".report-container").append(`
            <div class="report" id="`+ item["QID"] + `">
                <h2 class="report-question">`+ item["QID"] + ". " + item["question"] +`</h2>
                <div class="report-answers"></div>
            </div>
        `);
        item["answers"].forEach(function (answerItem, index) {
            $("#" + item["QID"]).find(".report-answers").append(`
                <h3><span class="answer-pretty-id">` + answerItem["prettyAID"] + `</span>`
                + answerItem["answer"] + `</h3>
                <p>` + answerItem["description"] + `</p>
            `);
        });
    });
}

/**
 * progress bar in navigation
 * @param minNumQ
 * @param answeredNumQ
 */
function updateProgressBar(minNumQ, answeredNumQ) {
    // TODO save some energy on calculate the exact progress for future
    // for now just roughly update
    var progress = "0";
    var percent = answeredNumQ / minNumQ;

    if (percent > 0 && percent < 0.3) progress = "5";
    else if (percent >= 0.3 && percent < 0.6) progress = "33";
    else if (percent >= 0.6 && percent <= 0.9) progress = "66";
    else if (percent > 0.9) progress = "99";

    $(".progress-bar").css("width", progress + "%").attr("aria-valuenow", progress);
    $("#progress-container p").text(progress + "% Complete");
}

$("#answers").on("click", ".answer", function () {
    // if radio button, also need to disable other selections first
    if ($("#answers").attr("multiple-answers") === "false") {
        $(".answer").removeClass("selected");
    }
    $(this).toggleClass("selected");
    var selection = $(this).find("input");
    selection.prop("checked") ? selection.prop("checked", false) : selection.prop("checked", true);
})

/**
 * update pastQNA
 * @param QID
 * @param AID
 * @param pastQNA
 * @returns {*}
 */
function addQNAtoHistory(QID, AID, pastQNA){
    let duplicated = false;
    for (i=0; i<pastQNA.length; i++){
        if (pastQNA[i]["QID"] === QID){
            duplicated = true;
            break;
        }
    }

    if (!duplicated){
        pastQNA.unshift({"QID": QID, "AID": AID});
    }

    return pastQNA
}