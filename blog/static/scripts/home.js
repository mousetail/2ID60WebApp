$(".postsummary").on('click', function(ev) {
   let id=$(ev.delegateTarget).attr("id");
   number=Number(id.substring(5))
   window.location.assign("/view/"+number)
})