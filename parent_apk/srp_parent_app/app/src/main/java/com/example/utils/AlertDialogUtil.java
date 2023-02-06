package com.example.utils;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;

import com.example.login.R;

public class AlertDialogUtil {
    private void dialog(Context context){
        //创建对话框并申明对象
        AlertDialog dialog = null;
        //绑定当前界面窗口，设置标题
        AlertDialog finalDialog = dialog;
        dialog = new AlertDialog.Builder(context)
                .setTitle("Dialog对话框")// 设置提示信息
                .setMessage("按钮1已被点击,是否退出")
                .setIcon(R.mipmap.msgbox)//设置图标
                .setPositiveButton("确定", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialogInterface, int i) {
                        finalDialog.dismiss();
                    }
                })
                .setNegativeButton("取消", null)
                .create(); // 创建对话框
        dialog.show();// 显示对话框
    }


}
