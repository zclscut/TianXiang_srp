package com.example.studentandroid;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.content.Intent;
import android.media.MediaRecorder;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.TextView;

import com.example.studentandroid.database.UserSqliteDBHelper;

public class LoginSuccessActivity extends AppCompatActivity implements View.OnClickListener {

    private ImageButton btn_back_main;
    private Button btn_start;
    private TextView tv_information;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login_success);
        //设置文本
        tv_information = findViewById(R.id.tv_information);
        //设置按键事件
        btn_back_main = findViewById(R.id.btn_back_main);
        btn_back_main.setOnClickListener(this);
        btn_start = findViewById(R.id.btn_start);
        btn_start.setOnClickListener(this);

        //从上一页面传来的意图中获取包裹
        Bundle bundle = getIntent().getExtras();
        String bd_mail = bundle.getString("bd_mail");
        String bd_password = bundle.getString("bd_password");
        if(bd_mail != null) {
            String desc = String.format("您的用户信息为： \n登录邮箱：%s\n密码：%s",bd_mail,bd_password);
            tv_information.setText(desc);
        }

    }


    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.btn_back_main:
                Intent intent = new Intent(this, MainActivity.class);
                intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
                startActivity(intent);
                break;

            case R.id.btn_start:
                //startActivity(new Intent(this, MediaRecordActivity.class));
                Intent intent2 = new Intent(this, MediaRecordActivity.class);
                intent2.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
                startActivity(intent2);
                break;

        }

    }
}