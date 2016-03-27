


$('#add-comment').hide()
$('#single').hide()
$('#add-comment').submit(function(event) {
    event.preventDefault();

    $.ajax({
        url: '/add_json',
        type: 'POST',
        dataType: 'json',
        data: $('#add-comment').serialize(),
        success: function(response){
            $('#get-comment-form').show()
            $('#add-comment').hide()
            $('#add-comment').each(function() {
                this.reset();
            });
        }
    });
    // author = $('#user').val()
    // console.log($('#comment').val())
    // console.log($('#add-comment'))
    // comment = $('#comment')



    // html =
    //          '<p id="author">  '+ author + ' </p>' +
    //          '<p id="authored"> Just added </p>'+
    //           '<p id="thoughts"> ' + comment + '</p>'
    // $('#new_comment').html(html)

});

$('#get-comment-form').on('click', function(){
    $('#add-comment').show()
    $('#get-comment-form').hide()
})


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
