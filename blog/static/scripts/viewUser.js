$("#changeProfilePic").on('click', function(ev) {
    ev.preventDefault();
    $("#profilePicForm").css("display","unset");
    $("#changeProfilePic").remove();
})