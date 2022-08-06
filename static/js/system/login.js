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
$('#login_btn').on('click',function (){
    var flag=login_check_username();
    if (!flag){
        return;
    }
    var pwd=login_check_password();
    if (!pwd){
        return;
    }
    //登录

})
//--------------------------------------登录end------------------------------------------------