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
            dataGridView1 = new DataGridView();
            Column1 = new DataGridViewTextBoxColumn();
            Column2 = new DataGridViewTextBoxColumn();
            Column3 = new DataGridViewTextBoxColumn();
            statusStrip1 = new StatusStrip();
            toolStripStatusLabel1 = new ToolStripStatusLabel();
            toolStripStatusLabel2 = new ToolStripStatusLabel();
            ((System.ComponentModel.ISupportInitialize)dataGridView1).BeginInit();
            statusStrip1.SuspendLayout();
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
            // dataGridView1
            // 
            dataGridView1.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dataGridView1.Columns.AddRange(new DataGridViewColumn[] { Column1, Column2, Column3 });
            dataGridView1.Location = new Point(310, 272);
            dataGridView1.Name = "dataGridView1";
            dataGridView1.RowHeadersWidth = 51;
            dataGridView1.RowTemplate.Height = 29;
            dataGridView1.Size = new Size(502, 319);
            dataGridView1.TabIndex = 10;
            dataGridView1.CellContentClick += dataGridView1_CellContentClick;
            // 
            // Column1
            // 
            Column1.HeaderText = "类别";
            Column1.MinimumWidth = 6;
            Column1.Name = "Column1";
            Column1.ReadOnly = true;
            Column1.Resizable = DataGridViewTriState.False;
            Column1.Width = 90;
            // 
            // Column2
            // 
            Column2.HeaderText = "事件";
            Column2.MinimumWidth = 6;
            Column2.Name = "Column2";
            Column2.Width = 150;
            // 
            // Column3
            // 
            Column3.HeaderText = "时间";
            Column3.MinimumWidth = 6;
            Column3.Name = "Column3";
            Column3.Width = 210;
            // 
            // statusStrip1
            // 
            statusStrip1.ImageScalingSize = new Size(20, 20);
            statusStrip1.Items.AddRange(new ToolStripItem[] { toolStripStatusLabel1, toolStripStatusLabel2 });
            statusStrip1.Location = new Point(0, 590);
            statusStrip1.Name = "statusStrip1";
            statusStrip1.Size = new Size(1155, 26);
            statusStrip1.TabIndex = 11;
            statusStrip1.Text = "statusStrip1";
            // 
            // toolStripStatusLabel1
            // 
            toolStripStatusLabel1.Name = "toolStripStatusLabel1";
            toolStripStatusLabel1.Size = new Size(167, 20);
            toolStripStatusLabel1.Text = "toolStripStatusLabel1";
            // 
            // toolStripStatusLabel2
            // 
            toolStripStatusLabel2.Name = "toolStripStatusLabel2";
            toolStripStatusLabel2.Size = new Size(167, 20);
            toolStripStatusLabel2.Text = "toolStripStatusLabel2";
            // 
            // Form2
            // 
            AutoScaleDimensions = new SizeF(9F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(1155, 616);
            Controls.Add(statusStrip1);
            Controls.Add(dataGridView1);
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
            FormBorderStyle = FormBorderStyle.FixedSingle;
            Name = "Form2";
            StartPosition = FormStartPosition.CenterScreen;
            Text = ".";
            ((System.ComponentModel.ISupportInitialize)dataGridView1).EndInit();
            statusStrip1.ResumeLayout(false);
            statusStrip1.PerformLayout();
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
        private DataGridView dataGridView1;
        private DataGridViewTextBoxColumn Column1;
        private DataGridViewTextBoxColumn Column2;
        private DataGridViewTextBoxColumn Column3;
        private StatusStrip statusStrip1;
        private ToolStripStatusLabel toolStripStatusLabel1;
        private ToolStripStatusLabel toolStripStatusLabel2;
    }
}