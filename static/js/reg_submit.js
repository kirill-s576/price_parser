$(document).ready(function () {
    $("#registration_submit").click(function () {
        let form_data = $(".registration-form");
        $.ajax({
            url: "/registration/",
            type: "POST",
            dataType: "html",
            data: form_data.serialize(),
            success: function(response){
                alert(response);
            },
            error: function (response) {
                alert("123");
            }
        });

    });
});