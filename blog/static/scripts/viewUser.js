$("#changeProfilePic").on('click', function(ev) {
    ev.preventDefault();
    $("#profilePicForm").append("<input name=\"photo\"/ placeholder=\"url\">", "<input type=\"submit\"/>")
})