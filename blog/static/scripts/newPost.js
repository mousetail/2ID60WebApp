$("#publish").on("click", function() {
    $("#id_pubType").attr("value", "publish");
});

$("#draft").on("click", function() {
    $("#id_pubType").attr("value", "draft");
})

$("#preview").on("click", function() {
    $("#id_pubType").attr("value", "preview");
})