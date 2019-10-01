$(document).ready(function () {


    $('form[name=key-form]').submit(function(event){
        event.preventDefault();
    });


    $(".ajax-submit").click(function () {
        let csrftoken = $("[name=csrfmiddlewaretoken]").val();
        let data = {
            keys: $(".parse-input").val()
        };
        $.ajax({
            url: "/ironparsermain/parse/",
            type: "POST",
            dataType: "html",
            headers:{
                "X-CSRFToken": csrftoken
            },
            data: data,
            success: function(response){
                $(".parse-container").html(response);
            },
            error: function (response) {
                alert("Ошибка");
            }
        });

    });


    $(".create-goose").click(function () {
        event.preventDefault();
        let data = [];
        $('input[type=checkbox]:checked').each(function() {
        let parentBlock = $(this).closest('div');
        console.log(parentBlock.find(".goose-price").text());
        let goose = {
                    name: parentBlock.find(".goose-name").text(),
                    price: parseFloat(parentBlock.find(".goose-price").text()),
                    url: parentBlock.find('a').attr('href'),
                    parent: parentBlock.parent().find('.goose-parent').text()

                    };
        data.push(goose);
        });
        let request = {
            "data": JSON.stringify(data),
            "keys": $(".parse-input").val(),
            "name": $(".new-goose-input").val(),
            "category": $(".goose-category-select").prop('selected', true).val()
        };
        let csrftoken = $("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            url: "/ironparsermain/create_goose/",
            type: "POST",
            dataType: "JSON",
            headers:{
                "X-CSRFToken": csrftoken
            },
            data: request,
            success: function(response){
                alert(response)
            },
            error: function (response) {
                alert("Ошибка");
            }
        });
    });


    $(".other-button").click(function () {
         event.preventDefault();
         let parentBlock = $(this).parent();
         if (parentBlock.find(".other-container").prop("hidden") === true){
             parentBlock.find(".other-container").prop("hidden",false);
         } else {
             parentBlock.find(".other-container").prop("hidden",true);
         }

     });

});

