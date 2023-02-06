package com.example.login;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Looper;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.EditText;
import android.widget.RadioGroup;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.example.utils.ConnectMySQL;

import java.util.Objects;

public class MineActivity extends AppCompatActivity {
    public static int loadingCounter=0;
    TextView mine_tel_email;
    RelativeLayout mine_info_set;
    RelativeLayout mine_about;
    RelativeLayout mine_version;
    RelativeLayout mine_back;
    RelativeLayout mine_exit;
    private SharedPreferences sp;//实现不同activity之间通信
    //
//    EditText parentName,studentName;
//    EditText parentSex,studentSex;
//    EditText parentPhone,studentPswd;
    //用户信息
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_mine);
        //去掉标题栏
        if (getSupportActionBar() != null){
            getSupportActionBar().hide();
        }
        //
        loadingCounter++;
        //初始化
        mine_tel_email= (TextView) findViewById(R.id.mine_tel_email);
        mine_info_set=(RelativeLayout) findViewById(R.id.mine_info_set);
        mine_about=(RelativeLayout) findViewById(R.id.mine_about);
        mine_version=(RelativeLayout) findViewById(R.id.mine_version);
        mine_back=(RelativeLayout) findViewById(R.id.mine_back);
        mine_exit=(RelativeLayout) findViewById(R.id.mine_exit);
        sp=getSharedPreferences("Personal", Context.MODE_PRIVATE);
        mine_tel_email.setText(sp.getString("tel_email",""));//从登录页面的Personal中取数据

        //执行监听
        executeClick();

    }

    private void executeClick(){
        //信息设置
        mine_info_set.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v)
            {   //----------进行父母信息填写------------------
                AlertDialog.Builder builder = new AlertDialog.Builder(MineActivity.this);
                builder.setIcon(R.mipmap.msgbox);
                builder.setTitle("请完善基本信息");
                //    通过LayoutInflater来加载一个xml的布局文件作为一个View对象
                View view = LayoutInflater.from(MineActivity.this).inflate(R.layout.dialog_parent_info, null);
                //    设置我们自己定义的布局文件作为弹出框的Content
                builder.setView(view);
                final EditText parentName= (EditText)view.findViewById(R.id.dialog_parent_name_edit);
                final EditText parentSex = (EditText)view.findViewById(R.id.dialog_parent_sex_edit);
                final EditText parentPhone=(EditText)view.findViewById(R.id.dialog_parent_phone_edit);
                final EditText studentName=(EditText)view.findViewById(R.id.dialog_student_name_edit);
                final EditText studentSex=(EditText)view.findViewById(R.id.dialog_student_sex_edit);
                final EditText studentPswd=(EditText)view.findViewById(R.id.dialog_student_pswd_edit);
                builder.setPositiveButton("确定", new DialogInterface.OnClickListener()
                {
                    @Override
                    public void onClick(DialogInterface dialog, int which)
                    {
                        String pname = parentName.getText().toString().trim();
                        String pphone=parentPhone.getText().toString().trim();
                        String psex=parentSex.getText().toString().trim();
                        String sname=studentName.getText().toString().trim();
                        String ssex=studentSex.getText().toString().trim();
                        String spswd=studentPswd.getText().toString().trim();

                        boolean setState=true;//设置信息的状态
                        if(pname.equals("")||pphone.equals("")||psex.equals("")||sname.equals("")||ssex.equals("")||spswd.equals("")){
                            Toast.makeText(MineActivity.this, "还有信息未完善", Toast.LENGTH_SHORT).show();
                        }else{
                            try{
                                setInfoMethod(pname,psex,pphone,sname,ssex,spswd);
                            }catch (Exception e){
                                setState=false;
                            }
                            //设置信息状态判断
                            if(setState){
                                Toast.makeText(MineActivity.this, "设置信息成功", Toast.LENGTH_SHORT).show();
//                                //    将输入的用户名和密码打印出来
//                                Toast.makeText(MineActivity.this, "用户名: " + pname+"\n号码:"+pphone+" 性别:"+psex
//                                        +"\n学生名:"+sname+"\n密码:"+spswd+" 性别:"+ssex, Toast.LENGTH_SHORT).show();
                            }else{
                                Toast.makeText(MineActivity.this, "设置信息失败,请检查网络", Toast.LENGTH_SHORT).show();
                            }
                        }

                    }
                });
                builder.setNegativeButton("取消", new DialogInterface.OnClickListener()
                {
                    @Override
                    public void onClick(DialogInterface dialog, int which)
                    {

                    }
                });
                builder.show();
            }
        });

        //关于app
        mine_about.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //R.string.app_about查询strings.xml中字符串
                Toast.makeText(MineActivity.this, R.string.app_about, Toast.LENGTH_SHORT).show();
            }
        });

        //版本
        mine_version.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //R.string.app_version查询strings.xml中字符串
                Toast.makeText(MineActivity.this, "当前的版本是:"+R.string.app_version, Toast.LENGTH_SHORT).show();
            }
        });

        //返回
        mine_back.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                startActivity(new Intent(MineActivity.this,MainActivity.class));
            }
        });
        //退出
        mine_exit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //创建对话框并申明对象
                AlertDialog dialog ;
                //绑定当前界面窗口，设置标题
                dialog = new AlertDialog.Builder(MineActivity.this)
                        .setTitle("Dialog对话框")// 设置提示信息
                        .setMessage("是否退出？")
                        .setIcon(R.mipmap.msgbox)//设置图标
                        .setPositiveButton("确定", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialogInterface, int i) {
                                Intent intent = new Intent(MineActivity.this,LoginActivity.class);
                                //传递退出所有Activity的Tag对应的布尔值为true
                                intent.putExtra(LoginActivity.EXIST, true);
                                //启动BaseActivity
                                startActivity(intent);
                            }
                        })
                        .setNegativeButton("取消", null)
                        .create(); // 创建对话框
                dialog.show();// 显示对话框
            }
        });

    }

    //设置信息的进程方法
    private void setInfoMethod(String pname,String psex,String pphone,String sname,String ssex,String spswd){
        new Thread(new Runnable() {
            @Override
            public void run() {
                //student_id和parent_id一致
                String tel_email=sp.getString("tel_email","");
                String sql1="select parent_id from parent_info where parent_email=? or parent_tel=?";
                new ConnectMySQL().doSql(sql1,2,new String[]{tel_email,tel_email},"query");
                int parent_id=Integer.parseInt(Objects.requireNonNull(ConnectMySQL.table.get(0).get("parent_id")));
                String sql2="update parent_info set parent_name=?,parent_sex=?,parent_tel=? where parent_id=?";
                new ConnectMySQL().doSql(sql2,4,new String[]{pname,psex,pphone,""+parent_id},"others");
                String sql3="update student_info set student_name=?,student_sex=?,student_pswd=? where student_id=?";
                new ConnectMySQL().doSql(sql3,4,new String[]{sname,ssex,spswd,""+parent_id},"others");
            }
        }).start();
    }


}