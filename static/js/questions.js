//enable tooltip
$('[data-toggle="tooltip"]').tooltip({html:true});

// Default root ID always 1
ROOT_QUESTION_ID = "1"

// assume pattern will be /module/questions
let moduleList = ["cleaning", "distancing", "data-infrastructure", "mask", "testing", "ventilation"]

// current module
module = $(location).attr('href').split("/").slice(-2)[0];
$(".module-name").empty().text(module);

// next module
var currModuleInd = moduleList.indexOf(module);
if (currModuleInd > -1 && currModuleInd < moduleList.length - 1) {
    var nextModule = moduleList[currModuleInd + 1]
    $(".next-module-name").text(nextModule)
    $("#next-module-btn").attr("href", `/${nextModule}/questions`)
} else {
    $(".next-module-name").text("Home");
}

// populate sidebar
$("#list-group-items").empty();
moduleList.forEach(function (m, i) {
    $("#list-group-items").append(`<a href="/` + m + `/questions" class="list-group-item list-group-item-action"
       id="sidenav-` + m + `">` + m + `</a>`
    );
    // set active module in sidenav
    $(".sidenav").find("#sidenav-" + module).addClass("active");
})

// get current date
var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
var yyyy = today.getFullYear();
$("#timestamp").empty().text(mm + '/' + dd + '/' + yyyy)

if (localStorage.getItem(module + "-QID") === null
    || localStorage.getItem(module + "-pastQNA") === null
){
    // intialized
    localStorage.setItem(module + "-QID", ROOT_QUESTION_ID);
    localStorage.setItem(module + "-pastQNA", "[]");
}

$(".module-menu").on("click", function(){
    $(".sidenav").toggleClass("active");
});

$(".overlay-block").on("click", function(){
    $(".sidenav").removeClass("active");
})

/**
 * update page when document ready
 */
$(document).ready(function () {
    $.ajax({
        url: "questions",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            "QID": localStorage.getItem(module + "-QID"),
            "qna": JSON.parse(localStorage.getItem(module + "-pastQNA"))
        }),
        success: function (data) {
            if ("page" in data) {
                localStorage.setItem(module + "-QID", data.page["QID"]);
            var answerNumQ = JSON.parse(localStorage.getItem(module + "-pastQNA")).length;
            updateQuestions(data, answerNumQ);
            } else if ("report" in data && "checklist" in data) {
                localStorage.setItem(module + "-QID", null);
                updateResult(data);
            }
        },
        error: function (jqXHR, exception) {
             window.location.href = "/error";
        }
    });
})


/**
 * submit the selection and go to next step
 */
$(".next button").on("click", function () {
    var QID = localStorage.getItem(module + "-QID");
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
                "qna": JSON.parse(localStorage.getItem(module + "-pastQNA"))
            }),
            success: function (data) {
                // add past question and answer to the stack
                let pastQNA = JSON.parse(localStorage.getItem(module + "-pastQNA"));
                updatedPastQNA = addQNAtoHistory(QID, AID, pastQNA)
                localStorage.setItem(module + "-pastQNA", JSON.stringify(updatedPastQNA));

                if ("page" in data) {
                    localStorage.setItem(module + "-QID", data.page["QID"]);
                    updateQuestions(data, pastQNA.length);
                } else if ("report" in data && "checklist" in data) {
                    localStorage.setItem(module + "-QID", null);
                    updateResult(data);
                }
            },
            error: function (jqXHR, exception) {
                window.location.href = "/error";
            }
        });
    } else {
        $("#alert").show();
    }

});

/**
 * going to the previous option
 */
$(".prev button").on("click", function () {
    // if alert on display, hide alert
    $("#alert").hide();

    // look at the stack top to see what's the preivous question ID
    let pastQNA = JSON.parse(localStorage.getItem(module + "-pastQNA"));
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
            localStorage.setItem(module + "-pastQNA", JSON.stringify(pastQNA));

            // update the current page id
            localStorage.setItem(module + "-QID", data.page["QID"]);
            updateQuestions(data, pastQNA.length);
        },
        error: function (jqXHR, exception) {
            window.location.href = "/error";
        }
    });
});


/**
 * jump to the root and restart the survey questions, clear all past histories
 */
$("#restart").on("click", function () {
    localStorage.setItem(module + "-QID", ROOT_QUESTION_ID);
    localStorage.setItem(module + "-pastQNA", "[]");
    $.ajax({
        url: "questions",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            "QID":localStorage.getItem(module + "-QID"),
            "qna":[]
        }),
        success: function (data) {
            updateQuestions(data, JSON.parse(localStorage.getItem(module + "-pastQNA")).length);
        },
        error: function (jqXHR, exception) {
             window.location.href = "/error";
        }
    });
});


/**
 * generate pdf for the report page
 */
$(".download-pdf").on("click", function () {
    html2pdf()
        .set({
            margin: 0.5,
            // pagebreak: {mode: ['css']},
            filename: "my-" + module + "-decision-report.pdf",
            jsPDF: {
                unit: 'in',
                format: 'letter',
                orientation: 'portrait'},
            html2canvas:{
                onclone: function (document){
                    var resultPDF = document.getElementsByClassName("result-pdf");
                    for (i=0; i<resultPDF.length; i++){
                        resultPDF[i].className += " print";
                    }
                },
                // ignore button
                ignoreElements: function (el){return el.tagName.toLowerCase() === "button"}},
        })
        .from(document.getElementById("result-pdf"))
        .save();
})

/**
 * expand and collapse answer description in report
 */
$(".report-container").on("click", "i", function(){
    $(this).hide();
    $(this).siblings("i").show();
    var answerDescription = $(this).parent().find(".report-answer-description");
    if (this.className.includes("expand")){
        answerDescription.show();
    }
    else if (this.className.includes("collapse")){
        answerDescription.hide();
    }
});

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
        $(".prev").hide();
    } else {
        $(".prev").show();
    }

    // enable next
    $(".next").show();

    // update progress bar
    updateProgressBar(data.minNumQ, answeredNumQ)

    // for questions
    var questionTitle = data.page["question"]
    $("#question-title").html(questionTitle);
    if ("multiple" in data.page && data.page["multiple"] === true){
        $("#answer-prompt").html("Select Multiple Answers");
    }
    else{
        $("#answer-prompt").html("Select One Answer");
    }
    $("#question-description").html(data.page["description"]);

    // for answers
    $("#answers").removeAttr("multiple-answers").empty();
    data.page["answers"].forEach(function(option, index){
        // do not display empty question
        if (option["answer"] !== ""){
            if ("multiple" in data.page && data.page["multiple"] === true) {
                var answer = $(`
                    <div class="answer">
                        <input type="checkbox" name="choice" value="` + option["AID"] + `">
                        <h2 class="answer-text" data-toggle="tooltip" data-placement="top" 
                                data-html="true" 
                                title="` + option["description"].replace(/<|>|"/g, "") +`">
                        <span class="answer-pretty-id">` + option["prettyAID"] +
                        `</span>` + option["answer"] + `</h2>
                        <p class="answer-description">` + option["description"] + `</p>
                    </div>`);
                $("#answers").attr("multiple-answers", true).append(answer);
            } else {
                var answer = $(`
                    <div class="answer">
                        <input type="radio" name="choice" value="` + option["AID"] + `">
                        <h2 class="answer-text" data-toggle="tooltip" data-placement="top" 
                                data-html="true" 
                                title="` + option["description"].replace(/<|>|"/g, "") +`">
                        <span class="answer-pretty-id">` + option["prettyAID"]
                        + `</span>` + option["answer"] + `</h2>
                        <p class="answer-description">` + option["description"] + `</p>
                    </div>`);
                $("#answers").attr("multiple-answers", false).append(answer);
            }

            // add recommended badge
            if ("recommended" in option && option["recommended"] === true) {
                answer.find("h2").after(`<div class="recommended" data-toggle="tooltip" 
                    data-placement="top" data-html="true" title="This is recommended.">
                    <i class="fas fa-star"></i></div>`);
            }
        }
        else{
             $("#answers").attr("multiple-answers", false).append(`<div class="answer" style="display:none;">
                <input type="radio" name="choice" value="` + option["AID"]+ `" hidden checked></div>`);
        }
    });
}


/**
 * update results container including checklist and report
 * @param data
 */
function updateResult(data) {
    $("#result-container").show();
    $("#qna-container").hide();

    // hide next
    $(".next").hide();

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
        var checkList =
            $(`<div class="checklist"><input type="checkbox"/>
            <p class="checklist-activity">` + item["activity"] +`</p>
            </div><hr>`);
        item["links"].forEach(function (link, index){
           checkList.find(".checklist-activity").after(`<a href="`+ link + `" target="_blank">` + link +`</a>`);
        });
        $(".checklists").append(checkList);       
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
                <h2 class="report-question">`+ item["question"] +`</h2>
                <div class="report-answers"></div>
            </div>
        `);
        item["answers"].forEach(function (answerItem, index) {
            $("#" + item["QID"]).find(".report-answers").append(`
                <div class="report-answer">
                    <i class="fas fa-caret-down report-expand"></i>
                    <i class="fas fa-caret-up report-collapse"></i>
                    <h3 class="report-answer-text"><span class="answer-pretty-id">` + answerItem["prettyAID"] + `</span>`
                    + answerItem["answer"] + `</h3>
                    <p class="report-answer-description">` + answerItem["description"] + `</p>
                </div>
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
    $("#progress-container p").html(progress + "% Complete");
}

/**
 * if any of the answer is selected
 */
$("#answers").on("click", ".answer", function () {
    // if any of them selected, dismiss the alert
    $("#alert").hide();

    // if radio button, also need to disable other selections first
    if ($("#answers").attr("multiple-answers") === "false") {
        $(".answer").removeClass("selected");
        $(".answer-description").removeClass("selected");
    }
    $(this).toggleClass("selected");
    if ($(this).find(".answer-description").html() !== ""){
        $(this).find(".answer-description").toggleClass("selected");
    }

    var selection = $(this).find("input");
    selection.prop("checked") ? selection.prop("checked", false) : selection.prop("checked", true);
})

/**
 * close the alert forcefully
 */
$("#alert-close").on("click", function(){
    $("#alert").hide();
});

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