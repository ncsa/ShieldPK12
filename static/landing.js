// GET start or resume
var modules = ["cleaning", "distancing", "data-infrastructure", "mask", "testing", "ventilation"];

modules.forEach(function (module, index) {
    let moduleQNA = localStorage.getItem(module);
    if (moduleQNA !== null && JSON.parse(moduleQNA).length > 0)
    {
        $("#" + module).html("Resume <i class=\"fas fa-arrow-right\"></i>");
    }
    else{
         $("#" + module).html("Start <i class=\"fas fa-arrow-right\"></i>");
    }
});