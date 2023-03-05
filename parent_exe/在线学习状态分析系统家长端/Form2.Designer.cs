namespace 在线学习状态分析系统家长端
{
    partial class Form2
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            label1 = new Label();
            dateTime1 = new DateTimePicker();
            dateTime2 = new DateTimePicker();
            label2 = new Label();
            label3 = new Label();
            label4 = new Label();
            emotion = new CheckBox();
            fatigue = new CheckBox();
            posture = new CheckBox();
            focus = new CheckBox();
            button1 = new Button();
            label5 = new Label();
            label8 = new Label();
            label6 = new Label();
            stuId = new Label();
            parName = new Label();
            result = new TextBox();
            SuspendLayout();
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("Microsoft YaHei UI", 24F, FontStyle.Regular, GraphicsUnit.Point);
            label1.Location = new Point(247, 43);
            label1.Name = "label1";
            label1.Size = new Size(662, 52);
            label1.TabIndex = 0;
            label1.Text = "在线学习状态分析系统（家长查询）";
            label1.Click += label1_Click;
            // 
            // dateTime1
            // 
            dateTime1.Location = new Point(295, 148);
            dateTime1.Name = "dateTime1";
            dateTime1.Size = new Size(250, 27);
            dateTime1.TabIndex = 1;
            dateTime1.ValueChanged += dateTimePicker1_ValueChanged;
            // 
            // dateTime2
            // 
            dateTime2.Location = new Point(575, 148);
            dateTime2.Name = "dateTime2";
            dateTime2.Size = new Size(250, 27);
            dateTime2.TabIndex = 2;
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Location = new Point(552, 152);
            label2.Name = "label2";
            label2.Size = new Size(15, 20);
            label2.TabIndex = 3;
            label2.Text = "-";
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.Location = new Point(220, 152);
            label3.Name = "label3";
            label3.Size = new Size(69, 20);
            label3.TabIndex = 4;
            label3.Text = "查询时间";
            // 
            // label4
            // 
            label4.AutoSize = true;
            label4.Location = new Point(220, 209);
            label4.Name = "label4";
            label4.Size = new Size(69, 20);
            label4.TabIndex = 4;
            label4.Text = "查询内容";
            // 
            // emotion
            // 
            emotion.AutoSize = true;
            emotion.Checked = true;
            emotion.CheckState = CheckState.Checked;
            emotion.Location = new Point(309, 212);
            emotion.Name = "emotion";
            emotion.Size = new Size(91, 24);
            emotion.TabIndex = 5;
            emotion.Text = "情绪分析";
            emotion.UseVisualStyleBackColor = true;
            // 
            // fatigue
            // 
            fatigue.AutoSize = true;
            fatigue.Checked = true;
            fatigue.CheckState = CheckState.Checked;
            fatigue.Location = new Point(436, 212);
            fatigue.Name = "fatigue";
            fatigue.Size = new Size(106, 24);
            fatigue.TabIndex = 5;
            fatigue.Text = "疲劳度分析";
            fatigue.UseVisualStyleBackColor = true;
            // 
            // posture
            // 
            posture.AutoSize = true;
            posture.Checked = true;
            posture.CheckState = CheckState.Checked;
            posture.Location = new Point(566, 212);
            posture.Name = "posture";
            posture.Size = new Size(91, 24);
            posture.TabIndex = 5;
            posture.Text = "坐姿分析";
            posture.UseVisualStyleBackColor = true;
            // 
            // focus
            // 
            focus.AutoSize = true;
            focus.Checked = true;
            focus.CheckState = CheckState.Checked;
            focus.Location = new Point(692, 212);
            focus.Name = "focus";
            focus.Size = new Size(106, 24);
            focus.TabIndex = 5;
            focus.Text = "专注度分析";
            focus.UseVisualStyleBackColor = true;
            // 
            // button1
            // 
            button1.Location = new Point(929, 209);
            button1.Name = "button1";
            button1.Size = new Size(63, 29);
            button1.TabIndex = 6;
            button1.Text = "查询";
            button1.UseVisualStyleBackColor = true;
            button1.Click += button1_Click;
            // 
            // label5
            // 
            label5.AutoSize = true;
            label5.Location = new Point(220, 265);
            label5.Name = "label5";
            label5.Size = new Size(69, 20);
            label5.TabIndex = 7;
            label5.Text = "查询结果";
            // 
            // label8
            // 
            label8.AutoSize = true;
            label8.Font = new Font("Microsoft YaHei UI", 10F, FontStyle.Regular, GraphicsUnit.Point);
            label8.Location = new Point(46, 46);
            label8.Name = "label8";
            label8.Size = new Size(48, 23);
            label8.TabIndex = 8;
            label8.Text = "家长:";
            // 
            // label6
            // 
            label6.AutoSize = true;
            label6.Font = new Font("Microsoft YaHei UI", 9F, FontStyle.Regular, GraphicsUnit.Point);
            label6.Location = new Point(36, 75);
            label6.Name = "label6";
            label6.Size = new Size(68, 20);
            label6.TabIndex = 8;
            label6.Text = "学生id：";
            // 
            // stuId
            // 
            stuId.AutoSize = true;
            stuId.Font = new Font("Microsoft YaHei UI", 9F, FontStyle.Regular, GraphicsUnit.Point);
            stuId.Location = new Point(95, 75);
            stuId.Name = "stuId";
            stuId.Size = new Size(18, 20);
            stuId.TabIndex = 8;
            stuId.Text = "0";
            // 
            // parName
            // 
            parName.AutoSize = true;
            parName.Font = new Font("Microsoft YaHei UI", 10F, FontStyle.Regular, GraphicsUnit.Point);
            parName.Location = new Point(95, 46);
            parName.Name = "parName";
            parName.Size = new Size(44, 23);
            parName.TabIndex = 8;
            parName.Text = "家长";
            // 
            // result
            // 
            result.Location = new Point(310, 272);
            result.Multiline = true;
            result.Name = "result";
            result.Size = new Size(515, 319);
            result.TabIndex = 9;
            // 
            // Form2
            // 
            AutoScaleDimensions = new SizeF(9F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(1155, 616);
            Controls.Add(result);
            Controls.Add(stuId);
            Controls.Add(label6);
            Controls.Add(parName);
            Controls.Add(label8);
            Controls.Add(label5);
            Controls.Add(button1);
            Controls.Add(focus);
            Controls.Add(posture);
            Controls.Add(fatigue);
            Controls.Add(emotion);
            Controls.Add(label4);
            Controls.Add(label3);
            Controls.Add(label2);
            Controls.Add(dateTime2);
            Controls.Add(dateTime1);
            Controls.Add(label1);
            Name = "Form2";
            Text = ".";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Label label1;
        private DateTimePicker dateTime1;
        private DateTimePicker dateTime2;
        private Label label2;
        private Label label3;
        private Label label4;
        private CheckBox emotion;
        private CheckBox fatigue;
        private CheckBox posture;
        private CheckBox focus;
        private Button button1;
        private Label label5;
        private Label label8;
        private Label label6;
        private Label stuId;
        private Label parName;
        private TextBox result;
    }
}