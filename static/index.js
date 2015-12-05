$(document).ready(function(){
    $(".create_form").validate({
        rules: {
            name: {
                required: true
            },
            starting_bid: {
                required: true,
                number: true
            },
            buyoff_price: {
                required: true,
                number: true
            },
            expires: {
                required: true
            }
        },
        messages: {
            name: {
                required: "Please insert the name of the lot."
            },
            starting_bid: {
                required: "Please insert the starting price.",
                number: "This got to be a number."
            },
            buyoff_price: {
                required: "Please insert buy-off price.",
                number: "This got to be a number."
            },
            expires: {
                required: "Please insert date of expiration."
            }
        }
    });

    $(".change_form").validate({
        rules: {
            name: {
                required: true
            },
            starting_bid: {
                required: true,
                number: true
            },
            buyoff_price: {
                required: true,
                number: true
            },
            expires: {
                required: true
            }
        },
        messages: {
            name: {
                required: "Please insert the name of the lot."
            },
            starting_bid: {
                required: "Please insert the starting price.",
                number: "This got to be a number."
            },
            buyoff_price: {
                required: "Please insert buy-off price.",
                number: "This got to be a number."
            },
            expires: {
                required: "Please insert date of expiration."
            }
        }
    });

    $(".bid_form").validate({
        rules: {
            price: {
                required: true,
                number: true
            }
        },
        messages: {
            price: {
                required: "Please insert the price of the bid.",
                number: "This got to be a number."
            }
        }
    });

    $('.datetimepicker').datetimepicker({
        format: 'YYYY-MM-DD HH:MM',
        minDate: new Date($.now())
    });

});