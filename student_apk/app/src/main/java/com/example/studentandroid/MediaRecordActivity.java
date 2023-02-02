package com.example.studentandroid;

import android.hardware.Camera;
import android.media.MediaRecorder;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.Surface;
import android.view.TextureView;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;

import androidx.appcompat.app.AppCompatActivity;

import java.io.File;
import java.io.IOException;

public class MediaRecordActivity extends AppCompatActivity implements View.OnClickListener {

    private TextureView textureView;
    private Button btn_record;
    private MediaRecorder mediaRecorder;
    private Camera camera;
    private ImageButton btn_back_login;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_media_record);
        textureView = findViewById(R.id.textureView);
        btn_record =findViewById(R.id.btn_record);
        btn_record.setOnClickListener(this);
        btn_back_login = findViewById(R.id.btn_back_login);
        btn_back_login.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        switch(v.getId()) {
            case R.id.btn_record:
                CharSequence text = btn_record.getText();
                if(TextUtils.equals(text,"开始")) {
                    btn_record.setText("结束");
                    camera = Camera.open();
                    camera.setDisplayOrientation(90);
                    camera.unlock();
                    mediaRecorder = new MediaRecorder();
                    mediaRecorder.setCamera(camera);
                    mediaRecorder.setAudioSource(MediaRecorder.AudioSource.MIC);//设置音频源 麦克风
                    mediaRecorder.setVideoSource(MediaRecorder.VideoSource.CAMERA);//设置视频源 摄像头
                    mediaRecorder.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4);//设置视频文件格式
                    mediaRecorder.setAudioEncoder(MediaRecorder.AudioEncoder.AAC);//设置音频编码
                    mediaRecorder.setVideoEncoder(MediaRecorder.VideoEncoder.H264);//设置视频编码
                    mediaRecorder.setOrientationHint(90);//视频旋转一定角度
                    mediaRecorder.setOutputFile(new File(getExternalFilesDir(""),"a.mp4").getAbsolutePath());//设置视频输出文件
                    mediaRecorder.setVideoSize(640,480);//设置视频大小
                    mediaRecorder.setVideoFrameRate(30);//设置视频帧率
                    mediaRecorder.setPreviewDisplay(new Surface(textureView.getSurfaceTexture()));//设置预览图像
                    try {
                        mediaRecorder.prepare();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                    mediaRecorder.start();

                }else {
                    btn_record.setText("开始");
                    mediaRecorder.stop();
                    mediaRecorder.release();
                    camera.stopPreview();
                    camera.release();
                }
                break;

            case R.id.btn_back_login:
                finish();
                break;
        }


    }
}