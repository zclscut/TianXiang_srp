package com.example.login;


import java.sql.*;
import java.util.HashMap;
import java.util.List;
import java.util.Objects;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Looper;
import android.util.Log;
import android.widget.AdapterView;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.Spinner;
import android.view.*;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.Button;

import com.example.utils.ConnectMySQL;
import com.example.utils.SendEmailUtil;


public class LoginActivity extends AppCompatActivity {
    private final String TAG="登录页面测试:";
    private EditText tel_email;
    private EditText password;
    private RadioButton rememberPswd;
    private TextView forgetPswd;
    private Button login_button;
    private Button register_button;
    private SharedPreferences sp;//记住密码实现
    private TextView aboutUse;//使用说明


    @SuppressLint("MissingInflatedId")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
//        requestWindowFeature(Window.FEATURE_NO_TITLE);//继承了AppCompatActivity失效
        setContentView(R.layout.activity_login);
        //去掉标题栏
        if (getSupportActionBar() != null){
            getSupportActionBar().hide();
        }

        //实例化控件对象
        tel_email=(EditText) findViewById(R.id.login_tel_email);
        password=(EditText) findViewById(R.id.login_password);
        rememberPswd=(RadioButton)findViewById(R.id.login_remember_pswd);
        forgetPswd=(TextView)findViewById(R.id.login_forget_pswd);
        login_button=(Button) findViewById(R.id.login_button);
        register_button=(Button)findViewById(R.id.login_register_button);
        sp=getSharedPreferences("Personal",MODE_PRIVATE);//设置个人sp，模式为私有
        aboutUse=(TextView)findViewById(R.id.login_about_use);//使用说明
        //判断有记住密码操作，进行账号密码填充
        rememberMethod();
        //执行监听
        executeClick();


    }

    //监听
    private void executeClick(){

        //忘记密码监听
        forgetPswd.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent=new Intent(LoginActivity.this,FindPasswordActivity.class);
//                intent.putExtra("tel_email",tel_email.getText().toString());//传递数据
                startActivity(intent);
            }
        });
        //登录按钮监听
        login_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String telEmail=tel_email.getText().toString();
                String pswd=password.getText().toString();
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        if(telEmail.equals("")||pswd.equals("")){
                            Looper.prepare();//进程中使用Toast需要在Looper中
                            Toast.makeText(LoginActivity.this, "账号或密码不能为空白", Toast.LENGTH_SHORT).show();
                            Looper.loop();
                        }else{
                            //查询
                            String sql="select parent_pswd from parent_info where parent_email=? or parent_tel=?";
                            new ConnectMySQL().doSql(sql,2,new String[]{telEmail,telEmail},"query");
                            Log.i(TAG,""+ConnectMySQL.table);
                        }
                    }
                }).start();

                //登录判断处理在进程外
                if(ConnectMySQL.table.toString().equals("[]")){//判断是否有查询结果
                    Toast.makeText(LoginActivity.this, "账号或密码错误", Toast.LENGTH_SHORT).show();
                }else{
                    for(HashMap<String,String>row:ConnectMySQL.table){
                        if(row.get("parent_pswd").equals(pswd)){
                            Toast.makeText(LoginActivity.this, "登录成功！", Toast.LENGTH_SHORT).show();

                            //实现记住密码
                            if(rememberPswd.isChecked()){
                                //记住密码勾选
                                sp.edit().putString("tel_email",telEmail).apply();
                                sp.edit().putString("password",pswd).apply();
                                sp.edit().putBoolean("ck_rememberPswd",true).apply();//点击了记住密码
                                sp.edit().apply();
                            }else{
                                //未勾选记住密码
                                sp.edit().putString("tel_email","").apply();
                                sp.edit().putString("password","").apply();
                                sp.edit().putBoolean("ck_rememberPswd",false).apply();
                                sp.edit().apply();
                            }

                            //携带信息的页面跳转
                            Intent intent=new Intent(LoginActivity.this,MainActivity.class);
//                            intent.putExtra("tel_email",telEmail);//将数据放入intent中
                            startActivity(intent);
                        }else{
                            Toast.makeText(LoginActivity.this, "账号或密码错误", Toast.LENGTH_SHORT).show();
                        }
                    }
                }



            }
        });

        //注册按钮监听
        register_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent=new Intent(LoginActivity.this,RegisterActivity.class);
//                intent.putExtra("tel_email",tel_email.getText().toString());//传递数据
                startActivity(intent);
            }
        });

        //使用说明监听
        aboutUse.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //创建对话框并申明对象
                AlertDialog dialog = null;
                //绑定当前界面窗口，设置标题
                AlertDialog finalDialog = dialog;
                dialog = new AlertDialog.Builder(LoginActivity.this)
                        .setTitle("使用说明")// 设置提示信息
                        .setMessage(R.string.app_about_use)
                        .setPositiveButton("确定", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialogInterface, int i) {
//                                finalDialog.dismiss();
                            }
                        })
                        .setNegativeButton("取消", null)
                        .create(); // 创建对话框
                dialog.show();// 显示对话框
            }
        });
    }

    //记住账号和密码
    private void rememberMethod(){
        boolean rememberPswdState=sp.getBoolean("ck_rememberPswd",false);
        if(rememberPswdState){
            //点击了记住密码
            tel_email.setText(sp.getString("tel_email",""));
            password.setText(sp.getString("password",""));
            rememberPswd.setChecked(true);
        }
    }

    //声明一个静态常量，用作退出BaseActivity的Tag
    public static final String EXIST = "exist";
    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        if (intent != null) {//判断其他Activity启动本Activity时传递来的intent是否为空
            //获取intent中对应Tag的布尔值
            boolean isExist = intent.getBooleanExtra(EXIST, false);
            //如果为真则退出本Activity
            if (isExist) {
                this.finish();
            }
        }
    }




}