// GET start or resume
// data is passed from flask endpoint
moduleList = [];
data.forEach(function (item, i) { moduleList.push(item["moduleName"]); });

moduleList.forEach(function (module, index) {
    let moduleQNA = localStorage.getItem(module + "-pastQNA");
    if (moduleQNA !== null && JSON.parse(moduleQNA).length > 0)
    {
        $("#" + module).html("Resume <i class=\"fas fa-arrow-right\"></i>");
    }
    else{
         $("#" + module).html("Start <i class=\"fas fa-arrow-right\"></i>");
    }
});