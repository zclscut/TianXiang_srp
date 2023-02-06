/* 1.调用fragment必须使用newInstance()方法,避免fragment中的信息无法传到activity中

 */
package com.example.login;

import android.content.Intent;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.MenuItem;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentActivity;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import com.example.login.fragment.EmotionFragment;
import com.example.login.fragment.FatigueFragment;
import com.example.login.fragment.FocusFragment;
import com.example.login.fragment.PostureFragment;
import com.google.android.material.bottomnavigation.BottomNavigationView;


public class MainActivity extends FragmentActivity {

    private BottomNavigationView mNavigationView;

    private FragmentManager mFragmentManager;

    private Fragment[] fragments;
    private int lastFragment;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mNavigationView = findViewById(R.id.main_navigation_bar);
        initFragment();
        initListener();

    }

    private void initFragment() {
        //必须使用newInstance(String param1,String param2)进行fragment初始化,param1和param2任意
        EmotionFragment emotionFragment = EmotionFragment.newInstance("aa","bb");

        FatigueFragment fatigueFragment = FatigueFragment.newInstance("aa","bb");
        PostureFragment postureFragment = PostureFragment.newInstance("aa","bb");
        FocusFragment focusFragment = FocusFragment.newInstance("aa","bb");

        fragments = new Fragment[]{emotionFragment, fatigueFragment, postureFragment, focusFragment};
        mFragmentManager = getSupportFragmentManager();
        //默认显示HomeFragment
        mFragmentManager.beginTransaction()
                .replace(R.id.main_page_container, emotionFragment)
                .show(emotionFragment)
                .commit();
    }

    private void initListener() {
        mNavigationView.setOnNavigationItemSelectedListener(new BottomNavigationView.OnNavigationItemSelectedListener() {
            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {
                switch (item.getItemId()) {
                    case R.id.emotion:
                        if (lastFragment != 0) {
                            MainActivity.this.switchFragment(lastFragment, 0);
                            lastFragment = 0;
                        }
                        return true;
                    case R.id.fatigue:
                        if (lastFragment != 1) {
                            MainActivity.this.switchFragment(lastFragment, 1);
                            lastFragment = 1;
                        }
                        return true;
                    case R.id.posture:
                        if (lastFragment != 2) {
                            MainActivity.this.switchFragment(lastFragment, 2);
                            lastFragment = 2;
                        }
                        return true;
                    case R.id.focus:
                        if (lastFragment != 3) {
                            MainActivity.this.switchFragment(lastFragment, 3);
                            lastFragment = 3;
                        }
                        return true;
                }
                return false;
            }
        });
    }

    private void switchFragment(int lastFragment, int index) {
        FragmentTransaction transaction = mFragmentManager.beginTransaction();
        transaction.hide(fragments[lastFragment]);
        if (!fragments[index].isAdded()){
            transaction.add(R.id.main_page_container,fragments[index]);
        }
        transaction.show(fragments[index]).commitAllowingStateLoss();
    }

    //实现fragment跳转到fragment
    public void jumpFatigueFragment() {
        FragmentManager fm = getSupportFragmentManager();
        FragmentTransaction transaction = fm.beginTransaction();
        transaction.replace(R.id.main_page_container, FatigueFragment.newInstance("aa","bb"));
        transaction.addToBackStack(null);
        transaction.commit();

    }

    //将从跳转前页面的数据传到EmotionFragment
//    public String getTelEmailLogin(){
//        return getIntent().getStringExtra("tel_email");
//    }


}

