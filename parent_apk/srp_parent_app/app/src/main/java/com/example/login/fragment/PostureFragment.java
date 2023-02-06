/*  创建一个自带的空的Fragment，然后在MainActivity中调用newInstance方法实例化,
    fragment必须依赖于特定的activity
    在fragment中使用getActivity()方法获取当前fragment绑定的activity
 */
package com.example.login.fragment;

import android.annotation.SuppressLint;
import android.app.AlertDialog;
import android.app.FragmentManager;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentActivity;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.example.login.LoginActivity;
import com.example.login.MainActivity;
import com.example.login.MineActivity;
import com.example.login.R;
import com.example.utils.ConnectMySQL;
import com.example.utils.LineChartUtil;
import com.example.utils.PieChartUtil;
import com.example.utils.SetDateTimeUtil;
import com.github.mikephil.charting.charts.LineChart;
import com.github.mikephil.charting.charts.PieChart;
import com.github.mikephil.charting.data.PieEntry;
import com.hh.timeselector.timeutil.datedialog.DateListener;
import com.hh.timeselector.timeutil.datedialog.TimeConfig;
import com.hh.timeselector.timeutil.datedialog.TimeSelectorDialog;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Objects;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link EmotionFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class PostureFragment extends Fragment {
    private final String[] TAG={"情绪页面","疲劳页面","坐姿页面","专注度页面"};//Log.i(String TAG,String msg)显示日志
    private final String[] lineChartLegendOption={"1积极/2中性/3消极","1清醒/2临界状态/3轻度疲劳/4中度疲劳/5重度疲劳",
            "1坐姿正常/2面朝前/3面朝下/4坐姿倾斜","1极专注/2专注/3不专注/4极不专注"};//所有折线图legend
    private List<List<String>> pieChartLegendOption=new ArrayList<>();//所有饼图legend
    private String lineChartLegend;//单个折线图legend
    private List<String> pieChartLegend;//单个饼图legend
    private int optionSelectIndex=0;//选中的查询类别,默认0

    private String TAGI=TAG[0];//Log日志输出的类别,默认情绪
    private AlertDialog queryOptionDialog;//查询类别选择弹窗
    private int setDateTimeId;//设置时间的ID，1设置开始时间，2设置结束时间
    private String startDateTime,endDateTime;//选择的开始和结束时间
    private ImageView headBarMenu;
    private TextView headBarTitle;
    private TextView fromDateTime;
    private TextView toDateTime;
    private PieChart pieChart;
    private Button startTimeBtn;
    private Button endTimeBtn;
    private Button queryBtn;
    private LineChart lineChart;
    private SharedPreferences sp;//查询登录/注册/找回密码页面保存的信息

    //emotion的查询数据
    private static List<String> emotionTimeList=new ArrayList<>();
    private static List<Integer> emotionValueList=new ArrayList<>();
    private static List<Integer> emotionCountList=new ArrayList<>();


    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";

    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;

    public PostureFragment() {
        // Required empty public constructor
    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param param1 Parameter 1.
     * @param param2 Parameter 2.
     * @return A new instance of fragment EmotionFragment.
     */
    // TODO: Rename and change types and number of parameters
    public static PostureFragment newInstance(String param1, String param2) {
        PostureFragment fragment = new PostureFragment();
        Bundle args = new Bundle();
        args.putString(ARG_PARAM1, param1);
        args.putString(ARG_PARAM2, param2);
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getArguments() != null) {
            mParam1 = getArguments().getString(ARG_PARAM1);
            mParam2 = getArguments().getString(ARG_PARAM2);
        }
    }

    @SuppressLint("MissingInflatedId")
    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_emotion, null);
        headBarMenu=view.findViewById(R.id.head_bar_menu);
        headBarTitle=view.findViewById(R.id.head_bar_title);headBarTitle.setText("情绪页面");
        fromDateTime=view.findViewById(R.id.from_datetime_text);
        toDateTime=view.findViewById(R.id.to_datetime_text);
        pieChart= view.findViewById(R.id.pie_chart);
        startTimeBtn = view.findViewById(R.id.start_time_button);
        endTimeBtn=view.findViewById(R.id.end_time_button);
        queryBtn=view.findViewById(R.id.emotion_query_button);
        lineChart=view.findViewById(R.id.line_chart);
        sp= getActivity().getSharedPreferences("Personal",Context.MODE_PRIVATE);
        //初始化
        init();
        //进入页面设置查询时间
        Toast.makeText(getActivity(), "请设置查询时间:结束时间大于开始时间", Toast.LENGTH_SHORT).show();
        //执行按钮监听
        executeClick();

        return view;
    }

    //参数初始化
    private void init(){
        //先进行类别选择
        queryOption();
        //参数初始化
        for(int i=0;i<lineChartLegendOption.length;i++){
            String str=lineChartLegendOption[i];
            String[] splitStr=str.split("/");
            List<String> strList=new ArrayList<>();
            //将数组元素传到List中
            for(int j=0;j<splitStr.length;j++){
                strList.add(splitStr[j]);
            }
            pieChartLegendOption.add(strList);
        }
    }

    private void executeClick(){
        //headBarTitle监听
        headBarTitle.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
//                Toast.makeText(getActivity(), "你点击了标题栏的标题", Toast.LENGTH_SHORT).show();
                queryOption();
            }
        });

        //headBarMenu监听
        headBarMenu.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //点击图标实现页面跳转,将MainActivity中数据传到MineActivity
                Intent intent=new Intent(getActivity(), MineActivity.class);
                //在MainActivity中设置方法，进行fragment和activity之间的通信
//                MainActivity mainActivity=(MainActivity) getActivity();
//                intent.putExtra("tel_email",mainActivity.getTelEmailLogin());
                startActivity(intent);
            }
        });
        //设置开始时间
        startTimeBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                setDateTimeId=1;
                setDateTime(getActivity(),"设置开始时间：","2023-02-02 23:24");
                Log.i(TAGI,"时间测试1:"+1);
            }
        });
        //设置结束时间
        endTimeBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                setDateTimeId=2;
                setDateTime(getActivity(),"设置结束时间：","2023-02-02 23:49");
                Log.i(TAGI,"时间测试2:"+2);
            }
        });
        //查询按钮监听
        queryBtn.setOnClickListener(new View.OnClickListener() {
            @RequiresApi(api = Build.VERSION_CODES.N)
            @Override
            public void onClick(View view) {
                //选择的开始和结束时间
                startDateTime=(String)fromDateTime.getText();
                endDateTime=(String)toDateTime.getText();
                Log.i(TAGI,"情绪查询按钮:"+startDateTime+"\n"+endDateTime);
                //
                SimpleDateFormat format=new SimpleDateFormat("yyyy-MM-dd HH:mm");
                //处理开始时间大于结束时间
                try {
                    Date date1 = format.parse(startDateTime);
                    Date date2= format.parse(endDateTime);
                    Long time1=date1.getTime();
                    Long time2=date2.getTime();
                    if(time1>=time2){
                        Toast.makeText(getActivity(), "开始时间不能大于结束时间", Toast.LENGTH_SHORT).show();
                    }else{
                        Log.i(TAGI,"查询时间段:"+startDateTime+"-"+endDateTime);
                    }
                } catch (ParseException e) {
                    Toast.makeText(getActivity(), "设置时间段出问题，请重新设置", Toast.LENGTH_SHORT).show();
                }

                //新开一个进程查询结果
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        getEmotionData(startDateTime,endDateTime);//getEmotionData("2023-02-02 23:24","2023-02-02 23:49");
                    }
                }).start();

                //图表显示异常处理
                try{
                    //饼状图实心
                    showPieChart();//显示Pie
                    showLineChart();//显示折线图
                }catch (Exception e){
                    Toast.makeText(getActivity(), "查询数据出错", Toast.LENGTH_SHORT).show();
                }
                //初始化:将List中数据全部清空
                emotionCountList.clear();
                emotionTimeList.clear();
                emotionValueList.clear();
            }
        });
    }


    //饼图
    private void showPieChart() {
        // 设置每份所占数量
        List<PieEntry> yvals = new ArrayList<>();
        Toast.makeText(getActivity(), "emotionCountList:"+emotionCountList, Toast.LENGTH_SHORT).show();
        int countZero=0;//emotionCountList中0的个数
        if(emotionCountList.size()>=1){
            for(int i=0;i<emotionCountList.size();i++){
                if(emotionCountList.get(i)==0){
                    countZero++;
                }
                yvals.add(new PieEntry((float)emotionCountList.get(i), pieChartLegend.get(i)));
            }
        }
        if(countZero!=emotionCountList.size()){
            //设置每份的颜色
            List<Integer> colors = new ArrayList<>();
            colors.add(Color.parseColor("#6785f2"));
            colors.add(Color.parseColor("#675cf2"));
            colors.add(Color.parseColor("#496cef"));
            colors.add(Color.parseColor("#3CB371"));
            colors.add(Color.parseColor("#aa63fa"));
            colors.add(Color.parseColor("#58a9f5"));
            colors.add(Color.parseColor("#4B0082"));
            PieChartUtil pieChartManagger = new PieChartUtil(pieChart);
            pieChartManagger.showSolidPieChart(yvals, colors);
        }
    }

    //折线图
    private void showLineChart(){
        LineChartUtil lineChartManager=new LineChartUtil(lineChart);
        //设置显示的legend图例
        List<String> legendNameList = new ArrayList<>();
        legendNameList.add(lineChartLegend);

        int count=emotionTimeList.size();
        //设置x轴的数据
        if(count>=1){
            ArrayList<Float> xValues = new ArrayList<>();
            for (int i = 0; i <count; i++) {
                xValues.add((float) i);
            }

            //设置y轴的数据()
            List<List<Float>> yValues = new ArrayList<>();

            //y1Value代表一条线的数据
            List<Float> y1Value = new ArrayList<>();
            for (int j = 0; j < count; j++) {
                float value = (float) (emotionValueList.get(j));
                y1Value.add(value);
            }
            yValues.add(y1Value);

            //设置颜色
            List<Integer> colorList = new ArrayList<>();
            colorList.add(Color.parseColor("#6785f2"));//"#eecc44"

            //设置x轴显示的字符串数组
            String[] xLabelList=new String[count];
            for(int i=0;i<count;i++){
                xLabelList[i]=i+"";//xLabelList[i]=emotionTimeList.get(i);
            }
            lineChartManager.showLineChart(6f,xLabelList,xValues, yValues, legendNameList, colorList);
        }else{
            Toast.makeText(getActivity(), "查询结果为空,请设置查询时间段", Toast.LENGTH_SHORT).show();
        }

    }

    @RequiresApi(api = Build.VERSION_CODES.N)
    private void getEmotionData(String startTime, String endTime){
        HashMap<String,Integer>emotionMap=new HashMap<>();//存放情绪类别出现的对应次数
        //初始化map
        List<String> sort=new ArrayList<>();
        switch (optionSelectIndex){
            case 0:sort.add("1");sort.add("2");sort.add("3");
                break;
            case 1:sort.add("1");sort.add("2");sort.add("3");sort.add("4");sort.add("5");
                break;
            case 2:sort.add("1");sort.add("2");sort.add("3");sort.add("4");
                break;
            case 3:sort.add("1");sort.add("2");sort.add("3");sort.add("4");
                break;
        }
        for(int i=0;i<sort.size();i++){
            emotionMap.put(sort.get(i),0);
        }

        //查询邮箱后号码对应的parent_id,parent_id和student_id一致
        String tel_email=sp.getString("tel_email","");
        String sql1="select parent_id from parent_info where parent_email=? or parent_tel=?";
        new ConnectMySQL().doSql(sql1,2,new String[]{tel_email,tel_email},"query");
        String parent_id=ConnectMySQL.table.get(0).get("parent_id");
        //查询id对应的内容
        String sql2="select record_time,state_value from study_state where student_id=? and state_key=? and  " +
                "record_time>=? and record_time<=? group by record_time";
        new ConnectMySQL().doSql(sql2,4,new String[]{parent_id,String.valueOf(optionSelectIndex+1),startTime,endTime},"query");

        //数据库查询结果
//        System.out.println(ConnectMySQL.table);
        for(int i=0;i<ConnectMySQL.table.size()-1;i++){
            String recordTime0 =ConnectMySQL.table.get(i).get("record_time");
            String recordTime1=ConnectMySQL.table.get(i+1).get("record_time");
            String time0 = recordTime0.substring(10, 19);//获取时间
            String time1 = recordTime1.substring(10, 19);//获取时间
            String valuestr=ConnectMySQL.table.get(i).get("state_value");

            //设置折线图的x轴时间和y轴情绪类别值
            emotionTimeList.add(time0);
            emotionValueList.add(Integer.valueOf(valuestr));

            //设置要读取的时间字符串格式
            SimpleDateFormat timeFormat = new SimpleDateFormat("HH:mm:ss");//设置时间格式
            Date date0 = null;
            Date date1 = null;
            try {
                date0 = timeFormat.parse(time0);
                date1 = timeFormat.parse(time1);
            } catch (ParseException e) {
                e.printStackTrace();
            }

            //转换为Date类
            Long timestamp0 = date0.getTime();//以毫秒为单位
            Long timestamp1 = date1.getTime();//以毫秒为单位
            int deltSecondInt=(int)((timestamp1-timestamp0)/1000);//将long型转换为int型
            Integer delta=Integer.valueOf(deltSecondInt);//将int型转换为Integer
//            System.out.println("delta--"+delta);
//            System.out.println("key--"+ConnectMySQL.table.get(i).get("event_value"));
//            System.out.println("mapValue--"+emotionMap.get(ConnectMySQL.table.get(i).get("event_value")));
            if(delta>10*60){
                //超过10分钟没有检测到数据，说明没有在测试
                emotionMap.replace(ConnectMySQL.table.get(i).get("state_value"),emotionMap.get(ConnectMySQL.table.get(i).get("state_value"))+1);
            }else{
                emotionMap.replace(ConnectMySQL.table.get(i).get("state_value"),emotionMap.get(ConnectMySQL.table.get(i).get("state_value"))+delta);
            }
        }

        //查询时间内每种情绪出现的次数
        for(Integer value:emotionMap.values()){
            emotionCountList.add(value);
        }
        Log.i(TAGI,"emotionCountList:"+emotionCountList);
        Log.i(TAGI,"emotionTimeList.size():"+emotionTimeList.size());
        Log.i(TAGI,"emotionValueList.size():"+emotionValueList.size());
    }

    //时间设置的方法:最小只能到分钟
    public void setDateTime(Context context, String title,String defaultDatetime){
        TimeSelectorDialog dialog = new TimeSelectorDialog(context);
        //设置标题
        dialog.setTimeTitle(title);
        //显示类型
        dialog.setIsShowtype(TimeConfig.YEAR_MONTH_DAY_HOUR_MINUTE);
        //默认时间
        dialog.setCurrentDate(defaultDatetime);
        //隐藏清除按钮
        dialog.setEmptyIsShow(false);
        //设置起始时间
        dialog.setStartYear(1900);
        dialog.setDateListener(new DateListener() {
            @Override
            public void onReturnDate(String time,int year, int month, int day, int hour, int minute, int isShowType) {
                Toast.makeText(context,time,Toast.LENGTH_LONG).show();
                //设置显示
                if(setDateTimeId==1){
                    fromDateTime.setText(time);
                }else{
                    toDateTime.setText(time);
                }
            }
            @Override
            public void onReturnDate(String empty) {
                Toast.makeText(context,empty,Toast.LENGTH_LONG).show();
                //设置显示
                if(setDateTimeId==1){
                    fromDateTime.setText(empty);
                }else{
                    toDateTime.setText(empty);
                }
            }});dialog.show();
    }

    public void queryOption(){
        final String[] items = {"情绪", "疲劳度", "坐姿", "专注度"};
        AlertDialog.Builder alertBuilder = new AlertDialog.Builder(getActivity());
        alertBuilder.setTitle("查询类别选择");
        alertBuilder.setSingleChoiceItems(items, 0, new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
//                Toast.makeText(getActivity(), items[i], Toast.LENGTH_SHORT).show();
                headBarTitle.setText(items[i]);
                optionSelectIndex=i;
                TAGI=TAG[i];
                lineChartLegend=lineChartLegendOption[i];
                pieChartLegend=pieChartLegendOption.get(i);
                Log.i(TAGI," optionSelectIndex:"+ optionSelectIndex);
                Log.i(TAGI,"lineChartLegend:"+lineChartLegend);
                Log.i(TAGI,"pieChartLegend:"+pieChartLegend);
                Toast.makeText(getActivity(), optionSelectIndex+"\n"+TAGI+"\n"+pieChartLegend+"\n"+lineChartLegend, Toast.LENGTH_SHORT).show();
            }
        });

        alertBuilder.setPositiveButton("确定", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {

            }
        });

        alertBuilder.setNegativeButton("取消", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {

            }
        });
        queryOptionDialog = alertBuilder.create();
        queryOptionDialog.show();
    }
}











