// 初始化修改密码dialog
$('#system_index_update_password_dialog').dialog({
    title: '修改密码',
    iconCls: 'icon-edit',
    resizable: false,
    draggable: false,   //不可拖拽
    modal: true,        //模态
    closed:true,       //是否关闭
    buttons:[{          //按钮
           text:'保存',
           iconCls:'icon-save',
            handler:function(){
                var flag=$('#system_index_update_password_form').form('validate');
                if(flag){
                    //提交表单
                    sub_system_index_update_form();

                    // 清除form对话框的值
                    $('#system_index_update_password_form input').val('');

                    //关闭dialog对话框
                    $('#system_index_update_password_dialog').dialog('close')
                }
            }
        },{
            text:'关闭',
            iconCls:'icon-cancel',
            handler:function(){
                $('#system_index_update_password_dialog').dialog('close')
            }
    }]
});

//点击修改密码弹出对话框
function open_update_password_dialog(username){
    //返显用户名
    $('#username').val(username)
    //弹出对话框
    $('#system_index_update_password_dialog').dialog('open')
}
// 提交修改密码表单
function sub_system_index_update_form(){
   $('#system_index_update_password_form').form('submit',{
        url:'/system/update_password/',
        success:function(result){
            var obj=JSON.parse(result)
            //显示提示信息
            $.messager.show({
            title:'提示',
            msg:obj.msg,
            timeout:5000,
            showType:'slide'
            });
            //退出系统，清除cookie，清除session
            if (200==obj.code){
                //前台清除cookie
                $.removeCookie('login_username_cookie',
                             {'expires':15,'path':'/','domain':'127.0.0.1'});

                //后台清除session

                setTimeout(function (){
                    window.location.href='/logout/'
                },2000);
            }

        }
    });
}

//安全退出 后台清除session
function logout(){
    //弹出提示框是否退出
    $.messager.confirm('是否退出', '您确定要退出系统吗?', function(r){
	if (r){
        //前台清除cookie 保留用户名
		$.removeCookie('login_password_cookie',
                         {'expires':15,'path':'/','domain':'127.0.0.1'})

        //请求后台
        window.location.href='/logout/'
	    }
    });
}

// 打开一个新页面
function openTab(title,urls,iconCls){
    //选项面板是否存在，存在选中，不存在添加
    var flag=$('#tabs').tabs('exists',title)
    if (flag){
        $('#tabs').tabs('select',title);
    }else{
        $('#tabs').tabs('add',{
        title:title,
        closable:true,  //是否可以关闭
        href:urls
        });
    }
}
