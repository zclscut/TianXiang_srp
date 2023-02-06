package com.example.login;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.CountDownTimer;
import android.os.Looper;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.example.utils.ConnectMySQL;
import com.example.utils.SendEmailUtil;

public class FindPasswordActivity extends AppCompatActivity {
    public static FindPasswordActivity findPasswordActivityInstance=null;
    private ImageView headBack;
    private TextView headTitle;
    private EditText emailEdit;
    private EditText verifyCodeEdit;
    private Button verifyCodeBtn;
    private EditText passwordEdit;
    private EditText passwordVerifyEdit;
    private Button findPswdBtn;
    private SharedPreferences sp;//实现页面之间的小数据量的通信

    private String receiver;//测试邮箱="fancilia20@gmail.com"
    private String getVerifyCode;

    private boolean downTimerState=false;//初始时，没验证码倒计时
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_find_password);
        //关闭
        findPasswordActivityInstance=this;
        //去掉标题栏
        if (getSupportActionBar() != null){
            getSupportActionBar().hide();
        }
        //实例化页面构件
        headBack=(ImageView)findViewById(R.id.head_bar_back);
        headTitle=(TextView) findViewById(R.id.head_bar_title);headTitle.setText("找回密码");//设置页面顶部标题
        emailEdit=(EditText) findViewById(R.id.email_input);
        verifyCodeEdit=(EditText)findViewById(R.id.verify_code_input);
        verifyCodeBtn=(Button) findViewById(R.id.verify_code_button);
        passwordEdit=(EditText)findViewById(R.id.password_input);
        passwordVerifyEdit=(EditText)findViewById(R.id.password_input_again);
        findPswdBtn=(Button)findViewById(R.id.find_pswd_button);
        //使用SharedPreferences进行activity之间通信
        sp=getSharedPreferences("Personal", Context.MODE_PRIVATE);
        emailEdit.setText(sp.getString("tel_email",""));

        //执行监听事件
        execute();

    }

    public void execute(){
        //返回图标监听
        headBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //跳转到登录页面
                startActivity(new Intent(FindPasswordActivity.this,LoginActivity.class));
            }
        });

        //获取验证码按钮监听
        verifyCodeBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        //使用进程查询
                        String sql="select * from parent_info where parent_email=?;";
                        new ConnectMySQL().doSql(sql,1,new String[]{emailEdit.getText().toString()},"query");

                        //判断邮箱是否存在
                        if(ConnectMySQL.table.size()==0){
                            //存在该邮箱账号,不允许注册
                            Looper.prepare();
                            Toast.makeText(FindPasswordActivity.this,"该邮箱不存在,请查看邮箱输入是否有误",Toast.LENGTH_SHORT).show();
                            Looper.loop();
                        }
                        else{
                            //不存在该账号,允许注册
                            if(!downTimerState){
                                downTimer.start();
                                new Thread(new Runnable() {
                                    @Override
                                    public void run() {
                                        if(sendVerifyCode()){
                                            //在进程中使用Toast需要进行Looper处理,防止内存泄露
                                            Looper.prepare();
                                            Toast.makeText(FindPasswordActivity.this,"发送邮箱验证码成功",Toast.LENGTH_SHORT).show();
                                            Looper.loop();
                                        }else{
                                            Looper.prepare();
                                            Toast.makeText(FindPasswordActivity.this,"发送邮箱验证码失败\n请检查网络或邮箱是否正确",Toast.LENGTH_SHORT).show();
                                            Looper.loop();
                                        }
                                    }
                                }).start();
                            }

                        }
                    }
                }).start();

            }

        });

        //找回密码按钮监听
        findPswdBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(verifyCodeEdit.getText().toString().equals(getVerifyCode)){
                    String pass1=passwordEdit.getText().toString();
                    String pass2=passwordVerifyEdit.getText().toString();
                    if(pass1.equals("")||pass2.equals("")){
                        Toast.makeText(FindPasswordActivity.this, "设置的密码不能为空", Toast.LENGTH_SHORT).show();
                    }else{
                        if(pass1.equals(pass2)){
                            boolean alterState=true;
                            try{
                                alterDataMethod(pass2,emailEdit.getText().toString(),emailEdit.getText().toString());
                            }catch (Exception e){
                                alterState=false;
                            }
                            //判断修改密码是否成功
                            if(alterState){
                                Toast.makeText(FindPasswordActivity.this, "密码设置成功", Toast.LENGTH_SHORT).show();
                                sp.edit().putString("tel_email",emailEdit.getText().toString()).apply();//传入设置的信息
                                sp.edit().putString("password",pass2).apply();
                                //跳转
                                Intent intent=new Intent(FindPasswordActivity.this,MainActivity.class);
//                            intent.putExtra("tel_email",emailEdit.getText().toString());
                                startActivity(intent);
                            }else{
                                Toast.makeText(FindPasswordActivity.this, "密码设置失败,请检查网络后重试", Toast.LENGTH_SHORT).show();
                            }

                        }else{
                            Toast.makeText(FindPasswordActivity.this, "两次设置的密码不一致", Toast.LENGTH_SHORT).show();
                        }
                    }
                }else{
                    Toast.makeText(FindPasswordActivity.this, "验证码输入错误", Toast.LENGTH_SHORT).show();
                }
            }
        });
    }

    public boolean sendVerifyCode(){
        boolean sendVerifyCodeState=false;
        try{
            receiver=emailEdit.getText().toString();
            System.out.println(receiver);
            String addInfo="这是APP的验证码,请不要告诉其他人";
            getVerifyCode=new SendEmailUtil().getVerifyCode();//验证码
            SendEmailUtil.sendEmail(receiver,"验证码",getVerifyCode+" "+addInfo);
            sendVerifyCodeState=true;
        }catch(Exception e){
            System.out.println("发送邮箱失败");
        }
        return sendVerifyCodeState;
    }

    //倒计时模块
    private CountDownTimer downTimer = new CountDownTimer(60 * 1000, 1000) {
        @Override
        public void onTick(long l) {
            downTimerState = true;
            verifyCodeBtn.setText((l / 1000) + "秒");
        }
        @Override
        public void onFinish() {
            downTimerState = false;
            verifyCodeBtn.setText("重新发送");
        }
    };

    //插入修改的密码
    private void alterDataMethod(String password,String parent_email,String parent_tel){
        new Thread(new Runnable() {
            @Override
            public void run() {
                String sql="update parent_info set parent_pswd=? where parent_email=? or parent_tel=?";
                new ConnectMySQL().doSql(sql,3,new String[]{password,parent_email,parent_tel},"others");
            }
        }).start();
    }
}