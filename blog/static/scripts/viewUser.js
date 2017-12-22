$("#changeProfilePic").on('click', function(ev) {
    ev.preventDefault();
    $("#profilePicForm").css("display","unset");
    /*$("#profilePicForm label").addClass("button");*/
    $("#profilePicForm input").change(function() {
        $("#profilePicForm").submit();
    })
    $("#changeProfilePic").remove();
})

$("#profilePicForm label").addClass("button");