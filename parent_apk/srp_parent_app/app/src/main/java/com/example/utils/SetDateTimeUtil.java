package com.example.utils;

import android.content.Context;
import android.widget.Toast;

import com.hh.timeselector.timeutil.datedialog.DateListener;
import com.hh.timeselector.timeutil.datedialog.TimeConfig;
import com.hh.timeselector.timeutil.datedialog.TimeSelectorDialog;

public class SetDateTimeUtil {
    private String dateTime;
    //context是activity
    public String setDateTime( Context context,String title,String defaultDateTime){
        TimeSelectorDialog dialog = new TimeSelectorDialog(context);
        //设置标题
        dialog.setTimeTitle(title);
        //显示类型
        dialog.setIsShowtype(TimeConfig.YEAR_MONTH_DAY_HOUR_MINUTE);
        //默认时间
        dialog.setCurrentDate(defaultDateTime);
        //隐藏清除按钮
        dialog.setEmptyIsShow(false);
        //设置起始时间
        dialog.setStartYear(1970);
        dialog.setDateListener(new DateListener() {
            @Override
            public void onReturnDate(String time,int year, int month, int day, int hour, int minute, int isShowType) {
                Toast.makeText(context,time,Toast.LENGTH_LONG).show();
                dateTime=""+isShowType;
            }
            @Override
            public void onReturnDate(String empty) {
                Toast.makeText(context,empty,Toast.LENGTH_LONG).show();
            }});dialog.show();

            return dateTime;
    }
}
