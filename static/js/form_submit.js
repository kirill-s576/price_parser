$(document).ready(function () {

    let results = $(".result-goose");
    $(".result-body").append(results.sort(function(a, b)
        {
            console.log(a);
            return $(a).find(".result-price").text() - $(b).find(".result-price").text()

        }));

    $('form[name=key-form]').submit(function(event){
        event.preventDefault();
    });


    $(".ajax-submit").click(function () {
        let csrftoken = $("[name=csrfmiddlewaretoken]").val();
        let spinner = $(".mdl-spinner");
        spinner.addClass("is-active");
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
                spinner.removeClass("is-active");

                let actual_gooses = $('.actual-goose');
                let actual_gooses_array = [];
                $.each(actual_gooses, function(){
                    actual_gooses_array.push($(this).attr('href').replace(/\//g,""));
                });
                let goose_containers = $(".goose-container");
                $.each(goose_containers, function(){
                    let goose_name = $(this).find("a").attr('href').replace(/\//g,"");
                    if (actual_gooses_array.indexOf(goose_name)>=0){
                        $(this).css('background', 'linear-gradient(to top right, #ffffff, #ff6d6b)');
                        console.log(goose_name);
                    };
                });

            },
            error: function (response) {
                alert("Ошибка парсинга");
                spinner.removeClass("is-active");
            }
        });

    });

    $(document).on('click','.goose-container', function () {
        if ($(event.target).is('a')){

        } else {
           $(this).addClass('goose-container-checked mdl-cell--1-col').removeClass('goose-container mdl-cell--2-col')
               .css('background','linear-gradient(to top right, #ffffff, #9ae8af)');
           $(".goose-bar").append($(this));
        };

        let elems = $(".goose-container-checked");
        $(".goose-bar").append(elems.sort(function(a, b)
        {
            return parseFloat($(a).find(".goose-price").text()) - parseFloat($(b).find(".goose-price").text())

        }));


    });

     $(document).on('click','.goose-container-checked', function () {
         if ($(event.target).is('a')){

         }
         else {
             $(this).addClass('goose-container mdl-cell--2-col').removeClass('goose-container-checked mdl-cell--1-col')
            .css('background','linear-gradient(to top right, #ffffff, #e4ff50)');
            let text = $(this).find('.goose-parent').text();
            let shop = $('h5:contains('+text+')').parent().find(".mdl-grid");
            shop.append($(this));
         };

    });

     $(document).on('click','.refresh-checked-button', function () {

         let gooses = $(".goose-container-checked");
         $.each(gooses, function() {
             $(this).addClass('goose-container mdl-cell--2-col').removeClass('goose-container-checked mdl-cell--1-col')
            .css('background','linear-gradient(to top right, #ffffff, #e4ff50)');
             let text = $(this).find('.goose-parent').text();
             let shop = $('h5:contains('+text+')').parent().find(".mdl-grid");
             shop.append($(this));
         });


    });


    $(".create-goose").click(function () {
        event.preventDefault();
        let data = [];
        let spinner = $(".mdl-spinner");
        spinner.addClass("is-active");
        let id = 0;
        if (typeof(goose_id) != "undefined"){
            id = goose_id;
        };
        $(".goose-container-checked").each(function() {
            let parentBlock = $(this);

            let goose = {
                        name: parentBlock.find(".goose-name").text(),
                        price: parseFloat(parentBlock.find(".goose-price").text()),
                        url: parentBlock.find('a').attr('href'),
                        parent: parentBlock.find('.goose-parent').text()
                        };
            data.push(goose);
            });
        let request = {
            "id": id,
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
                alert("Товар добавлен!");
                let gooses = $(".goose-container-checked");
                 $.each(gooses, function() {
                     $(this).addClass('goose-container mdl-cell--2-col').removeClass('goose-container-checked mdl-cell--1-col')
                    .css('background','linear-gradient(to top right, #ffffff, #e4ff50)');
                     let text = $(this).find('.goose-parent').text();
                     let shop = $('h5:contains('+text+')').parent().find(".mdl-grid");
                     shop.append($(this));
                 });
                 $('#exampleModalLong').modal('toggle');
                 spinner.removeClass("is-active");
            },
            error: function (response) {
                alert("Ошибка добавления товара.");
                spinner.removeClass("is-active");
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

    $(".remove_op").click(function () {
        let button = $(this);
        let op_id = $(this).val();
        let data ={
            op_id: op_id
        };
        let csrftoken = $("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            url: "/ironparsermain/remove_op_goose/",
            type: "POST",
            dataType: "json",
            headers:{
                "X-CSRFToken": csrftoken
            },
            data: data,
            success: function(response){
                button.closest('tr').remove();
                $(".toast").toast('show');
            },
            error: function () {
                alert("Ошибка удаления товара.")
            }
        });
     });

    $(".add-goose-button").click(function () {
        $('#myModal').modal({
          keyboard: false
        });
        $('#exampleModalLong').modal('toggle');
    });

    $(".settings-button").click(function () {
        $('#myModal').modal({
          keyboard: false
        });
        $('#exampleModalLong').modal('toggle');
    });


    let func;
    $('#find').on('keyup', function () {
        clearTimeout(func);
        let template = $(this).val();
        data = {
            template: template
        };
        func = setTimeout(function () {
            if (template.length > 1){
                $.ajax({
                    url: "/ironparsermain/find_goose/",
                    type: "POST",
                    dataType: "html",
                    headers:{
                        "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
                    },
                    data: data,
                    success: function(response){
                        $(".findresult").empty();
                        $(".findresult").append(response);
                    },
                    error: function () {
                    }
                });
            }
        }, 1000)
    });

    $(".add-potential").click(function () {
        let potential_id = $(this).val();
        let parentBlock = $(this).closest('tr');
        data = {
            id: potential_id,
            goose_id: goose_id
        };
        $.ajax({
            url: "/ironparsermain/add_potential/",
            type: "POST",
            dataType: "json",
            headers:{
                "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
            },
            data: data,
            success: function(response){

                parentBlock.remove();
            },
            error: function () {
                alert("Что-то пошло не так");
            }
        });
    });

    $(".remove-potential").click(function () {
        let potential_id = $(this).val();
        let parentBlock = $(this).closest('tr');
        data = {
            id: potential_id
        };
        $.ajax({
            url: "/ironparsermain/remove_potential/",
            type: "POST",
            dataType: "json",
            headers:{
                "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
            },
            data: data,
            success: function(response){

                console.log(parentBlock);
                parentBlock.remove();
            },
            error: function () {
                alert("Что-то пошло не так");
            }
        });
    });

    $(".rem-all-potential").click(function () {
        data = {
            goose_id: goose_id
        };
        $.ajax({
            url: "/ironparsermain/remove_all_potential/",
            type: "POST",
            dataType: "json",
            headers:{
                "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
            },
            data: data,
            success: function(response){
                $(".pot-goose-tbody").empty();
            },
            error: function () {
                alert("Что-то пошло не так");
            }
        });
    });
});

