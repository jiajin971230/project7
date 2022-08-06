 //---------------------------验证用户名 start-----------------------------------------------------
         function check_username(){
             //获取用户名
             var flag=false;
             var username=$('#username').val()
             //验证用户名 字母或者字母加数字，必须字母开头
             var reg=/^[a-zA-Z][a-zA-Z0-9]{4,16}$/
             if (!reg.test(username)){
                 $('#reg_username').html('用户名必须是字母开头4-16位！');
                 return flag
             }else {
                 //用户名合法后清空提示
                 $('#reg_username').hide()
                  //发送ajax请求验证用户名唯一
                 $.ajax({
                     'type':'POST',
                     'url':'/system/unique_username/',
                     'data':{
                         'csrfmiddlewaretoken':$.cookie('csrftoken'),
                         'username':username
                     },
                     'dataType':'json',
                     'async':false, //ajax设置为同步
                     'success':function (result){
                         $('#reg_username').show()
                         //如果是400设置为false返回
                         if (400==result.code){
                             flag=false;
                             $('#reg_username').html(result.msg)
                         }
                         //如果是200就正常显示
                         if (200==result.code){
                             $('#reg_username').html(result.msg);
                             flag=true
                         }

                     },
                     'error':function (result){
                         console.log(result)
                     }
                });
                 //返回标记
                 return flag;
             }
         }
         $('#username').on('blur',check_username)
         //---------------------------验证用户名 end-----------------------------------------------------

        //---------------------------验证邮箱长度，丢失焦点事件start-------------------------------------------
         function check_email(){
             var flag=false;
             //获取邮箱
             var email=$('#email').val();
            $('#reg_span').show()
            //非空判断
            if (''==$.trim(email)||'邮 箱:'==$.trim(email)||null==$.trim(email)||undefined==$.trim(email)){
                $('#reg_span').html('邮箱不能为空！');
                return flag;
            }else{
                //验证邮箱
                var reg =/^([\.a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/;
                if (!reg.test(email)){
                    $('#reg_span').html('邮箱格式错误！');
                    return flag
                    }else {
                    //合法后清空提示
                    $('#reg_span').hide()
                    $.ajax({
                     'type':'POST',
                     'url':'crm/system/unique_username/',
                     'data':{
                         'csrfmiddlewaretoken':$.cookie('csrftoken'),
                         'email':email
                     },
                     'dataType':'json',
                     'async':false, //ajax设置为同步
                     'success':function (result){
                         $('#reg_span').show()
                         //如果是400设置为false返回
                         if (400==result.code){
                             flag=false;
                             $('#reg_span').html(result.msg)
                         }
                         //如果是200就正常显示
                         if (200==result.code){
                             $('#reg_span').html(result.msg);
                             flag=true
                         }

                     },
                     'error':function (result){
                         console.log(result)
                     }
                });
                    return flag
                }
            }
         }
         $('#email').on('blur',check_email)
        //---------------------------验证用户名长度，丢失焦点事件end-------------------------------------------
        //---------------------------验证密码 start--------------------------------------------------------
         function check_password(){
             //获取密码
            var pwd=$('#pwd').val()
            $('#reg_pwd').show()
            //输入值必须按照密码格式
             // 必须数字大小写特殊字符组成,最少8位 最多16位
            var reg =/^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)(?=.*?[#@*&.])[a-zA-Z\d#@*&.]{8,16}$/;
            if (!reg.test(pwd)){
                $('#reg_pwd').html("密码必须数字大小写特殊字符组成,最少8位 最多16位!")
                return false
            }else {
                 //合法后清空提示
                $('#reg_pwd').hide()
                return true
            }
         }
        $('#pwd').on('blur',check_password)
        //---------------------------验证密码 end----------------------------------------------------------
        //---------------------------重复验证密码 start-----------------------------------------------------
         function check_password2(){
            //获取密码
            var pwd=$('#pwd').val().trim()
             //获取重复密码
            var cpwd=$('#cpwd').val().trim()
            //获取提示字段
            var reg_pwd=$('#reg_pwd').val()
            $('#reg_cpwd').show()
            //非空判断
            if (undefined==cpwd || '' ==cpwd){
                $('#reg_cpwd').html('重复密码不能为空')
                return false
            }else {
                //进行比对
               if(cpwd !=pwd ){
                    $('#reg_cpwd').html('两次输入的密码不一致')
                   return false
                } else{
                   //合法后清空提示
                $('#reg_cpwd').hide()
                   return true
               }
            }
         }
        $('#cpwd').on('blur',check_password2)
        //---------------------------重复验证密码 end-------------------------------------------------------
    //点击注册按钮再次验证数据合法性
         $('#reg_btn').on('click',function (){
             //点击注册之后置灰
            $('#reg_btn').attr('disabled',true)
             //验证
            var flag= check_username();
             if (!flag){
                 return
             }
             var flag1= check_email();
             if (!flag1){
                 return
             }
             var flag2= check_password();
             if (!flag2){
                 return
             }
             var flag3= check_password2();
             if (!flag3){
                 return
             }
             //合法的话 发送邮件 激活账号
             //获取密码
             var pwd=$('#pwd').val().trim()
             //获取用户名
             var username=$('#username').val()
             //获取邮箱
             var email=$('#email').val();
             $.ajax({
                     'type':'POST',
                     'url':'/system/send_email/',
                     'data':{
                         'csrfmiddlewaretoken':$.cookie('csrftoken'),
                         'email':email,
                         'username':username,
                         'password':pwd
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
                             $('#reg_span').html(result.msg);
                         }

                     },
                     'error':function (result){
                         console.log(result)
                     }
                });
         })