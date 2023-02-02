package com.example.studentandroid;

import android.Manifest;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import com.example.studentandroid.database.User;
import com.example.studentandroid.database.UserSqliteDBHelper;
import com.example.studentandroid.util.ViewUtil;

public class MainActivity extends AppCompatActivity implements View.OnClickListener, View.OnFocusChangeListener {


    private EditText et_mail;
    private EditText et_password;
    private Button btn_login;
    private CheckBox ck_remember;
    private String mPassword = "123123";
    private UserSqliteDBHelper mHelper;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        //申请权限
        ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.CAMERA,Manifest.permission.RECORD_AUDIO},100);
        //给输入框添加文本变更监听器
        et_mail = findViewById(R.id.et_mail);
        et_password = findViewById(R.id.et_password);
        et_mail.addTextChangedListener(new HideTextWatcher(et_mail, 11));
        et_password.addTextChangedListener(new HideTextWatcher(et_password, 6));
        et_password.setOnFocusChangeListener(this);
        //给按键设置点击事件
        btn_login = findViewById(R.id.btn_login);
        btn_login.setOnClickListener(this);
        ck_remember = findViewById(R.id.ck_remember);

    }

    //重新填入信息
    public void reload() {
        User user = mHelper.queryTop();
        if (user != null && user.remember) {
            et_mail.setText(user.mail);
            et_password.setText(user.password);
            ck_remember.setChecked(true);
        }

    }

    //数据库连接
    @Override
    protected void onStart() {
        super.onStart();
        //获取数据库帮助器实例
        mHelper = UserSqliteDBHelper.getInstance(this);
        //打开读写连接
        mHelper.openWriteLink();
        mHelper.openReadLink();
        reload();
    }

    @Override
    protected void onStop() {
        super.onStop();
        mHelper.closelink();
    }


    //点击按钮后的事件
    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.btn_login:
                if (!mPassword.equals(et_password.getText().toString())) {
                    Toast.makeText(this,"请输入正确的密码", Toast.LENGTH_SHORT).show();
                    return;
                }
                LoginSuccess();
                break;
            default:
                break;
        }
    }

    //密码验证成功
    private void LoginSuccess() {
        String desc = String.format("您的邮箱是：%s，点击'确定'确认登录", et_mail.getText().toString());
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("登陆成功");
        builder.setMessage(desc);
        builder.setPositiveButton("确定", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                Intent intent = new Intent(MainActivity.this, LoginSuccessActivity.class);
                //传递包裹数据
                Bundle bundle = new Bundle();
                bundle.putString("bd_mail", et_mail.getText().toString());
                bundle.putString("bd_password", et_password.getText().toString());
                intent.putExtras(bundle);

                //执行页面跳转
                intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
                startActivity(intent);
            }
        });
        builder.setNegativeButton("返回 ",null);
        AlertDialog dialog = builder.create();
        dialog.show();

        //保存到数据库中
        User user = new User();
        user.mail = et_mail.getText().toString();
        user.password = et_password.getText().toString();
        user.remember = ck_remember.isChecked();
        mHelper.save(user);
    }

    //通过设置焦点监听，根据输入邮箱查询对应密码
    @Override
    public void onFocusChange(View v, boolean hasFocus) {
        if(v.getId() == R.id.et_password && hasFocus) {
            User user = mHelper.queryByMail(et_mail.getText().toString());
            if(user != null) {
                et_password.setText(user.password);
                ck_remember.setChecked(user.remember);
            }else{
                et_password.setText("");
                ck_remember.setChecked(false);
            }
        }
    }

    //收回键盘（文本变更监听）
    private class HideTextWatcher implements TextWatcher {
        private EditText mView;
        private int Maxlength;
        public HideTextWatcher(EditText v, int maxlength) {
            this.mView = v;
            this.Maxlength = maxlength;
        }

        @Override
        public void beforeTextChanged(CharSequence s, int start, int count, int after) {

        }

        @Override
        public void onTextChanged(CharSequence s, int start, int before, int count) {

        }

        @Override
        public void afterTextChanged(Editable s) {
            String str = s.toString();
            if(str.length() == Maxlength) {
                ViewUtil.hideOneInputMethod(MainActivity.this, mView);

            }
        }
    }
}