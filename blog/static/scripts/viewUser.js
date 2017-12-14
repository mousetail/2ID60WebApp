$("#changeProfilePic").on('click', function(ev) {
    ev.preventDefault();
    $("#profilePicForm").append("<input name=\"photo\"/ placeholder=\"url\" type=\"text\">", "<button type=\"submit\">Change picture</button>")
})