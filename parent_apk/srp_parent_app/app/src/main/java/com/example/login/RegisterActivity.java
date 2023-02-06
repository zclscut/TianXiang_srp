package com.example.login;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.CountDownTimer;
import android.os.Looper;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.example.utils.ConnectMySQL;
import com.example.utils.SendEmailUtil;

import java.util.Objects;

public class RegisterActivity extends AppCompatActivity {
    private String TAG="注册页面";
    public static RegisterActivity registerActivityInstance=null;
    private ImageView headBack;
    private TextView headTitle;
    private EditText tel_emailEdit;
    private EditText verifyCodeEdit;
    private Button verifyCodeBtn;
    private EditText passwordEdit;
    private EditText passwordVerifyEdit;
    private Button registerBtn;
    private SharedPreferences sp;//实现页面之间少量信息通信

    private String receiver;//测试邮箱="fancilia20@gmail.com"
    private String getVerifyCode;

    private boolean downTimerState=false;//初始时，没验证码倒计时
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);
        //关闭
        registerActivityInstance=this;
        //去掉标题栏
        if (getSupportActionBar() != null){
            getSupportActionBar().hide();
        }
        //实例化页面构件
        headBack=(ImageView)findViewById(R.id.head_bar_back);
        headTitle=(TextView) findViewById(R.id.head_bar_title);headTitle.setText("账号注册");//设置页面顶部标题
        tel_emailEdit=(EditText) findViewById(R.id.email_input);
        verifyCodeEdit=(EditText)findViewById(R.id.verify_code_input);
        verifyCodeBtn=(Button) findViewById(R.id.verify_code_button);
        passwordEdit=(EditText)findViewById(R.id.password_input);
        passwordVerifyEdit=(EditText)findViewById(R.id.password_input_again);
        registerBtn=(Button)findViewById(R.id.register_button);
        //使用SharedPreferences进行activity之间通信
        sp=getSharedPreferences("Personal", Context.MODE_PRIVATE);
        tel_emailEdit.setText(sp.getString("tel_email",""));

        //执行监听事件
        execute();

    }

    public void execute(){
        //返回图标监听
        headBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //跳转到登录页面
                startActivity(new Intent(RegisterActivity.this,LoginActivity.class));
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
                        new ConnectMySQL().doSql(sql,1,new String[]{tel_emailEdit.getText().toString()},"query");

                        //判断邮箱是否存在
                        if(ConnectMySQL.table.size()>=1){
                            //存在该邮箱账号,不允许注册
                            Looper.prepare();
                            Toast.makeText(RegisterActivity.this,"该邮箱已被注册,请选择其他邮箱",Toast.LENGTH_SHORT).show();
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
                                            Toast.makeText(RegisterActivity.this,"发送邮箱验证码成功",Toast.LENGTH_SHORT).show();
                                            Looper.loop();
                                        }else{
                                            Looper.prepare();
                                            Toast.makeText(RegisterActivity.this,"发送邮箱验证码失败\n请检查网络或邮箱是否正确",Toast.LENGTH_SHORT).show();
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

        //注册按钮监听
        registerBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(verifyCodeEdit.getText().toString().equals(getVerifyCode)){
                    String pass1=passwordEdit.getText().toString();
                    String pass2=passwordVerifyEdit.getText().toString();
                    boolean registerState;
                    if(pass1.equals("")||pass2.equals("")){
                        Toast.makeText(RegisterActivity.this, "设置的密码不能为空", Toast.LENGTH_SHORT).show();
                    }else{
                        if(pass1.equals(pass2)){
                            //信息传输
                            sp.edit().putString("tel_email",tel_emailEdit.getText().toString()).apply();
                            sp.edit().putString("password",pass2).apply();

                            boolean state=true;//注册状态
                            try{
                                insertDateMethod(pass2);
                            }catch (Exception e){
                                state=false;
                            }
                            //判断是否信息插入成功
                            if(state){
                                //页面跳转
                                Toast.makeText(RegisterActivity.this, "注册成功", Toast.LENGTH_SHORT).show();
                                Toast.makeText(RegisterActivity.this, "请完善信息", Toast.LENGTH_SHORT).show();
                                Intent intent=new Intent(RegisterActivity.this,MineActivity.class);
                                startActivity(intent);
                            }else{
                                Toast.makeText(RegisterActivity.this, "注册出错,请检查网络是否连接", Toast.LENGTH_SHORT).show();
                            }

                        }else{
                            Toast.makeText(RegisterActivity.this, "两次设置的密码不一致", Toast.LENGTH_SHORT).show();
                        }
                    }
                }else{
                    Toast.makeText(RegisterActivity.this, "验证码输入错误", Toast.LENGTH_SHORT).show();
                }
            }
        });
    }

    private void insertDateMethod(String pass2){
        //新开一个线程写入数据
        new Thread(new Runnable() {
            @Override
            public void run() {
                //student_id和parent_id一致
                String sql1="select max(parent_id) as max_id from parent_info";//查询最大parent_id
                new ConnectMySQL().doSql(sql1,1,new String[]{""},"query1");//无参查询
                int parent_id;
                if(ConnectMySQL.table.get(0).get("max_id")==null){
                    //表中没有数据
                    parent_id=1;
                }else{
                    parent_id=Integer.parseInt(Objects.requireNonNull(ConnectMySQL.table.get(0).get("max_id")))+1;
                }
                String sql2="insert into student_info values(?,?,?,?)";//除了id以外，其余均用"-"代替,最后在信息完善模块设置信息
                new ConnectMySQL().doSql(sql2,4,new String[]{""+parent_id,"-","-","-"},"others");
                String sql3="insert into parent_info values(?,?,?,?,?,?,?)";
                new ConnectMySQL().doSql(sql3,7,new String[]{""+parent_id,"-","-","-",tel_emailEdit.getText().toString(),pass2,""+parent_id},"others");
            }
        }).start();
    }


    public boolean sendVerifyCode(){
        boolean sendVerifyCodeState=false;
        try{
            receiver=tel_emailEdit.getText().toString();
            Log.i(TAG,"注册者:"+receiver);
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
}