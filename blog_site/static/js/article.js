
function selectOnchang(obj) {
    var value = obj.options[obj.selectedIndex].value;
    alert(value);
}

$("#save_article").click(function () {
    console.log("save_article------------dfdsfs----- event");
    var article_name = $("#title_input").val();
    var categary = $("#categary").val();
    console.log("save_article event" + categary);
    var ue = UE.getEditor('editor');
    var article_content = ue.getContent();
    var article_desc = ue.getPlainTxt();
    var source = "my website"
    $.ajax({
        type:"POST",
        url: "saveArticles",
        data: {"article_name" : article_name,
               "article_content": article_content,
               "article_desc": article_desc,
               "category_id": categary,
               "source": source},
        cache:false, //不缓存此页面
        success: function (data) {
            console.log("saveArticle response:" + data.result+"" + data.message)
            if (data.result == 200) {
               toastr.success('温馨提示', data.message);
               window.location.href='index';
            } else {
               //错误
               toastr.error('温馨提示', data.message);
            }
        }
    });
});