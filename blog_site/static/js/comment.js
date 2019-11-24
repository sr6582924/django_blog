$(function () {

        var article_id = GetQueryString("id");
        console.log("article_id" + article_id);
        $.ajax({
            url: "getCommentList",
            datatype: 'json',
            type: "get",
            data:{"article_id": article_id, "page": 0},
            success: function (data) {

                if (data != null) {
                    console.log("data" + JSON.stringify(data));
                    var list = data.data;
                    console.log("itemssssss" + list);
                    for (var i = 0; i < list.length; i++) {
                        var item = list[i];
                        $("#commentlist").append("<li class=\"comment-content\"><span class=\"comment-f\">#1</span>\n" +
                            "   <div class=\"comment-avatar\"><img class=\"avatar\" src=\"static/images/icon/icon.png\" alt=\"\" /></div>\n" +
                            "   <div class=\"comment-main\">\n" +
                            "     <p>"+item.user.userName+"<span class=\"time\">"+ formatDateTime(item.create_time)+"</span><br />\n" +
                            ""+item.comment+"</p>\n" +
                            "   </div>\n" +
                            " </li>");
                    }

                    var currentPage = data.currentPage; //得到currentPage
                    var totalPage = data.totalPage; //取到pageCount的值(把返回数据转成object类型)
                    console.log("pageCount:" + totalPage + " currentPage:" + currentPage)
                    var options = {
                        bootstrapMajorVersion: 2, //版本
                        currentPage: currentPage, //当前页数
                        totalPages: totalPage, //总页数
                        itemTexts: function (type, page, current) {
                            switch (type) {
                                case "first":
                                    return "首页";
                                case "prev":
                                    return "上一页";
                                case "next":
                                    return "下一页";
                                case "last":
                                    return "末页";
                                case "page":
                                    return page;
                            }
                        },//点击事件，用于通过Ajax来刷新整个list列表
                        onPageClicked: function (event, originalEvent, type, page) {
                            var article_id = GetQueryString("id");
                            console.log("article_id" + article_id);
                            $.ajax({
                                url: "getCommentList",
                                type: "get",
                                data:{"article_id": article_id, "page": (page-1)},
                                success: function (data1) {
                                    if (data1 != null) {
                                        $("#commentlist").empty();
                                        console.log("data" + JSON.stringify(data1));
                                        var list = data1.data;
                                        console.log("itemssssss" + list);
                                        for (var i = 0; i < list.length; i++) {
                                            var item = list[i];
                                            $("#commentlist").append("<li class=\"comment-content\"><span class=\"comment-f\">#1</span>\n" +
                                                "   <div class=\"comment-avatar\"><img class=\"avatar\" src=\"static/images/icon/icon.png\" alt=\"\" /></div>\n" +
                                                "   <div class=\"comment-main\">\n" +
                                                "     <p>"+item.user.userName+"<span class=\"time\">"+ formatDateTime(item.create_time)+"</span><br />\n" +
                                                ""+item.comment+"</p>\n" +
                                                "   </div>\n" +
                                                " </li>")
                                        }
                                    }
                                }
                            });
                        }
                    };
                    $('#example').bootstrapPaginator(options);
                }
            }
        });
    })