 //设置显示配置
var messageOpts = {
    "closeButton" : true,//是否显示关闭按钮
    "debug" : false,//是否使用debug模式
    "positionClass" : "toast-bottom-right",//弹出窗的位置
    "onclick" : null,
    "showDuration" : "300",//显示的动画时间
    "hideDuration" : "1000",//消失的动画时间
    "timeOut" : "2000",//展现时间
    "extendedTimeOut" : "1000",//加长展示时间
    "showEasing" : "swing",//显示时的动画缓冲方式
    "hideEasing" : "linear",//消失时的动画缓冲方式
    "showMethod" : "fadeIn",//显示时的动画方式
    "hideMethod" : "fadeOut" //消失时的动画方式
};
toastr.options = messageOpts;
//登录
$("#loginbtn").click(function () {
    $("#loginModal").modal('hide');
    console.log("login event");
    var userName = $("#loginUserName").val();
    var password = $("#loginPwd").val();
    console.log("login input userName" + userName + "password" + password);
    $.ajax({
        type:"POST",
        url: "login",
        data: {"userName" : userName , "password": hex_sha1(password)},
        cache:false, //不缓存此页面
        success: function (data) {
            console.log("login response:" + data.result+"" + data.message)
            if (data.result == 200) {
               //成功
               toastr.success('提示', '登录成功');
               setTimeout(function () {
                 window.location.reload()
               }, 1000);
            } else {
               //错误
               toastr.error('提示', data.message);
            }
        }
    });
});
//注册
$("#registerbtn").click(function () {
    $("#registerModal").modal('hide');
    var userName = $("#registerUserNmae").val();
    var password = $("#registerPwd").val();
    var tryPassword = $("#registerTryPwd").val();
    if (password != tryPassword) {
        toastr.error('提示', '二次输入密码不一致');
        return;
    }
    var email = $("#registerEmail").val();
    console.log("login input userName" + userName + "password" + password);
    $.ajax({
        type:"POST",
        url: "register",
        data: {"userName" : userName , "password": hex_sha1(password),"email": email },
        cache:false, //不缓存此页面
        success: function (data) {
            console.log("login response:" + data.result)
            if (data.result == 200) {
               //成功
               toastr.success('提示', '注册成功');
               setTimeout(function () {
                 window.location.reload()
               }, 1000);
            } else {
               //错误
               toastr.error('提示', data.message);
            }
        }
    });
});
//登出
$("#logoutbtn").click(function () {
    $("#registerModal").modal('hide');
    $.ajax({
        type:"POST",
        url: "logout",
        data: {},
        cache:false, //不缓存此页面
        success: function (data) {
            console.log("login response:" + data.result)
            if (data.result == 200) {
               //成功
               toastr.success('提示', '登出成功');
               setTimeout(function () {
                 window.location.reload()
               }, 1000);

            } else {
               //错误
               toastr.error('提示', data.message);
            }
        }
    });
});

function formatDateTime(inputTime) {
    var date = new Date(inputTime);
    var y = date.getFullYear();
    var m = date.getMonth() + 1;
    m = m < 10 ? ('0' + m) : m;
    var d = date.getDate();
    d = d < 10 ? ('0' + d) : d;
    var h = date.getHours();
    h = h < 10 ? ('0' + h) : h;
    var minute = date.getMinutes();
    var second = date.getSeconds();
    minute = minute < 10 ? ('0' + minute) : minute;
    second = second < 10 ? ('0' + second) : second;
    return y + '-' + m + '-' + d+' '+h+':'+minute+':'+second;
};

function GetQueryString(name)
{
     var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
     var r = window.location.search.substr(1).match(reg);
     if(r!=null)return  unescape(r[2]); return null;
}