//---------------------------验证用户名长度，丢失焦点事件start-------------------------------------------
function login_check_username(){
    //获取用户名
    username=$('#username').val().trim();
    $('#reg_span').show()
    //非空判断
    if (''==$.trim(username)||'用户名:'==$.trim(username)||null==$.trim(username)||undefined==$.trim(username)){
        $('#reg_span').html('请输入用户名！');
        return false;
    }else{
        //验证用户名
        var reg =/^[a-zA-Z][a-zA-Z0-9]{4,16}$/;
        if (!reg.test(username)){
            $('#reg_span').html('用户名不符合规范！');
            return false
            }else {
            $('#reg_span').hide()
            return true
        }
    }
}

$('#username').on('blur',login_check_username)

//---------------------------验证用户名长度，丢失焦点事件end-------------------------------------------

//--------------------------------------验证密码事件start-------------------------------------------
function login_check_password(){
    //获取密码
    pwd=$('#pwd').val().trim();
    $('#reg_pwd').show()
    //非空判断
    if (''==$.trim(pwd)||'密码:'==$.trim(pwd)||null==$.trim(pwd)||undefined==$.trim(pwd)){
        $('#reg_pwd').html('请输入密码！');
        return false;
    }
    $('#reg_pwd').hide()
    return true
}

$('#pwd').on('blur',login_check_password)

//--------------------------------------验证密码事件end-------------------------------------------
//--------------------------------------登录start----------------------------------------------
function login_user(){
    var flag=login_check_username();
    var username=$('#username').val()
    var password=$('#pwd').val()
    if (!flag){
        return;
    }
    var pwd=login_check_password();
    if (!pwd){
        return;
    }
    // 判断是否选择了"记住密码"
    var remember = $('#remember').is(':checked')

    //---------------------登录的ajax------------------
    $.ajax({
         'type':'POST',
         'url':'/system/login_user/',
         'data':{
             'csrfmiddlewaretoken':$.cookie('csrftoken'),
             'username':username,
             'password':password,
             'remember':remember
         },
         'dataType':'json',
         'async':false, //ajax设置为同步
         'success':function (result){
             $('#reg_span').show()
             //如果是400设置为false返回
             if (400==result.code){
                 $('#reg_span').html(result.msg)
             }
             //如果是200就正常显示
             if (200==result.code){
                 //如果用户选择了记住密码，
                 if (!(undefined==result.login_username_cookie || null==result.login_username_cookie||
                       undefined==result.login_password_cookie || null==result.login_password_cookie)){
                     //存储cookie 有效期为15天
                     $.cookie('login_username_cookie',result.login_username_cookie,
                         {'expires':15,'path':'/','domain':'127.0.0.1'})
                     $.cookie('login_password_cookie',result.login_password_cookie,
                         {'expires':15,'path':'/','domain':'127.0.0.1'})
                 }
                 window.location.href='/index/'
             }
         },
         'error':function (result){
             console.log(result)
         }
    })
}

$('#login_btn').on('click',login_user)

// --------------------选择记住密码时填充------------------
// 进入页面就执行的方法
$(function (){
    //获取login_cookie信息，展示到登录框
    var login_username_cookie =$.cookie('login_username_cookie');
    var login_password_cookie =$.cookie('login_password_cookie');
    //判断是否存在cookie
    if (!(undefined==login_username_cookie || null==login_username_cookie||undefined==login_password_cookie || null==login_password_cookie)){
        //base64解密cookie
        //正常点击记住密码后到这
        login_username_cookie=$.base64.decode(login_username_cookie);
        login_password_cookie=$.base64.decode(login_password_cookie);
        $('#username').val(login_username_cookie)
        $('#pwd').val(login_password_cookie)
    }else {
        //安全退出后到这
        login_username_cookie=$.base64.decode(login_username_cookie);
        $('#username').val(login_username_cookie)
    }
    //实现xx天免登录
})
//--------------------------------------登录end------------------------------------------------