$("#regress").on("click", function (e){
    var module = localStorage.getItem("module");
    if (module !== null) {
        e.preventDefault();
        window.location.href = "/regress?module=" + module;
    }
});