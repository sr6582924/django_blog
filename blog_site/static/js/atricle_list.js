$(".content-list").autobrowse({
        url:function (offset) {
            var url = "findArticleList?page="+offset;
            var category_id = GetQueryString('category_id')
            if (category_id)
                url += "&category_id=" + category_id;
            var keyword = GetQueryString('keyword')
            if (keyword)
                url += "&keyword=" + keyword;
            console.log("findArticleList url:" + url)
            return url;
        }, template:function (response) {
            //异步组装服务器端返回的数据
            setupArticleList(response);
        },
         itemsReturned:function (response) {
            //返回服务端数据的长度
             return response.data.length;
        },
        offset:0,
        max:1000,
        loader:'<div class="pagination-loading"><img src="/static/images/loading.gif" /></div>', //加载的图标,
        useCache:false, //使用缓存
        expiration:1,//过期时间
        sensitivity: 1, //触发下一页的差值
        finished: function () { $(this).append('<p style="text-align:center">加载完成，没   有更多活动了</p>') }//没有数据时的提示
    });

function setupArticleList(items) {
    for (var i = 0; i < items.data.length; i++) {
        var item = items.data[i];
        if (!item.category) {
            item.category= {id: 0, category_name:'默认分类'}
        }
        var article_name = item.article_name;
        console.log("article_name" + article_name.length)
        if(article_name.length > 30){
          article_name = article_name.substring(0, 30);
          article_name += "..."
          console.log("article_name" + article_name)
        }

        var article_desc = item.article_desc;
        var dd = article_desc.replace(/<\/?.+?>/g,"");
        article_desc = dd.replace(/ /g,"");//dds为得到后的内容
        if(article_desc.length > 200){
          article_desc = article_desc.substring(0, 200);
          article_desc += "..."
          console.log("article_desc" + article_desc)
        }
        $(".content-list").append("<article class=\"excerpt excerpt-1\">\n" +
            "          <a class=\"focus\" href=\"findArticleContent\" title=\"\"><img class=\"thumb\" data-original=\"/static/images/excerpt.jpg\" src=\"/static/images/excerpt.jpg\" alt=\"\"></a>\n" +
            "        <header><a class=\"cat\" href=\"program\">"+item.category.category_name+"<i></i></a>\n" +
            "          <h2><a href=\"getArticleContent?id="+item.id +"\" title=\"\">"+article_name+"</a></h2>\n" +
            "        </header>\n" +
            "        <p class=\"meta\">\n" +
            "          <time class=\"time\"><i class=\"glyphicon glyphicon-time\"></i>"+formatDateTime(item.create_time)+"</time>\n" +
            "          <span class=\"views\"><i class=\"glyphicon glyphicon-eye-open\"></i> 共"+item.watched+"人围观</span> <a class=\"comment\" href=\"findArticleContent\"><i class=\"glyphicon glyphicon-comment\"></i> 0个不明物体</a></p>\n" +
            "        <p class=\"note\">"+article_desc+"</p>\n" +
            "      </article>")
    }

}



