// search UIN
$("#search-bar input").keypress(function (e) {
    if (e.which === 13) {
        var uin = $(this).val();
        if (uin !== "" && uin !== undefined) {
            $.ajax({
                url: "search",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({
                    "uin": uin
                }),
                success: function (data) {
                    updateCurrentStatus(data.user)
                },
                error: function (jqXHR, exception) {
                    $("#current-status").hide().empty();
                    $("#error").find(".modal-body").empty().append(jqXHR.responseText);
                    $("#error").modal("show");
                }
            });
        } else {
            alert("You have to enter UIN to search!");
        }
    }
});

// search UIN
$("#search-bar button").on("click", function () {
    var uin = $("#search-bar input").val();
    if (uin !== "" && uin !== undefined) {
        $.ajax({
            url: "search",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                "uin": uin
            }),
            success: function (data) {
                updateCurrentStatus(data.user)
            },
            error: function (jqXHR, exception) {
                $("#current-status").hide().empty();
                $("#error").find(".modal-body").empty().append(jqXHR.responseText);
                $("#error").modal("show");
            }
        });
    } else {
        alert("You have to enter UIN to search!");
    }
});

// quarantine button
$("#quarantine").on("click", function(){
    submitActions("quarantine");
});

// isolate button
$("#isolate").on("click", function(){
    submitActions("isolate");
});

// release button
$("#release").on("click", function(){
    submitActions("release");
});

// update the status of the searched user (pink area)
function updateCurrentStatus(user) {
    $("#current-status").empty().append(
        `<h4>` + user["family_name"] + ", " + user["given_name"] + `</h4>
        <h4>UIN: ` + user["uin"] + `</h4>
        <p>Current Entry Status = ` + user["status"] + `</p>`
    ).show();
}

// action buttons
function submitActions(action){
    var uin = $("#search-bar input").val();
    if (uin !== "" && uin !== undefined) {
        $.ajax({
            url: action,
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                "uin": uin
            }),
            success: function (data) {
                 alert("Successfully "+ action  + " the current user: " + data["user"]["uin"] + "!")
                updateCurrentStatus(data.user)
            },
            error: function (jqXHR, exception) {
                $("#current-status").hide().empty();
                $("#error").find(".modal-body").empty().append(jqXHR.responseText);
                $("#error").modal("show");
            }
        });
    } else {
        alert("You have to enter the UIN in search box first!");
    }
}

