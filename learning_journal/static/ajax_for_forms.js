
$('#add-comment').submit(function(event) {
    event.preventDefault();

    $.ajax({
        url: '/add_json',
        type: 'POST',
        dataType: 'json',
        data: $('#add-comment').serialize(),
        success: function(response){
            console.log(response);
        }
    });
});

// $('#update-post').submit(function(event) {
//     event.preventDefault();

//     $.ajax({
//         url: '/post_json',
//         type: 'POST',
//         dataType: 'json',
//         data: $('#update-post').serialize(),
//         success: function(response){
//             console.log(response);
//         }
//     });
// });
