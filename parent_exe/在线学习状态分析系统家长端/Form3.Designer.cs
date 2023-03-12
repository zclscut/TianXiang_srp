namespace 在线学习状态分析系统家长端
{
    partial class Form3
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
            button1 = new Button();
            button2 = new Button();
            label1 = new Label();
            phoneNumber = new TextBox();
            passWord1 = new TextBox();
            passWord2 = new TextBox();
            label2 = new Label();
            label3 = new Label();
            label4 = new Label();
            parentName = new TextBox();
            parentEmail = new TextBox();
            label5 = new Label();
            label6 = new Label();
            radioButton1 = new RadioButton();
            radioButton2 = new RadioButton();
            studentID = new TextBox();
            label7 = new Label();
            SuspendLayout();
            // 
            // button1
            // 
            button1.Location = new Point(185, 389);
            button1.Name = "button1";
            button1.Size = new Size(94, 29);
            button1.TabIndex = 0;
            button1.Text = "返回";
            button1.UseVisualStyleBackColor = true;
            button1.Click += button1_Click;
            // 
            // button2
            // 
            button2.Location = new Point(294, 389);
            button2.Name = "button2";
            button2.Size = new Size(94, 29);
            button2.TabIndex = 0;
            button2.Text = "注册";
            button2.UseVisualStyleBackColor = true;
            button2.Click += button2_Click;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("Microsoft YaHei UI", 18F, FontStyle.Regular, GraphicsUnit.Point);
            label1.Location = new Point(220, 24);
            label1.Name = "label1";
            label1.Size = new Size(137, 39);
            label1.TabIndex = 1;
            label1.Text = "家长注册";
            // 
            // phoneNumber
            // 
            phoneNumber.Location = new Point(185, 185);
            phoneNumber.Name = "phoneNumber";
            phoneNumber.Size = new Size(203, 27);
            phoneNumber.TabIndex = 2;
            // 
            // passWord1
            // 
            passWord1.Location = new Point(185, 261);
            passWord1.Name = "passWord1";
            passWord1.Size = new Size(203, 27);
            passWord1.TabIndex = 2;
            // 
            // passWord2
            // 
            passWord2.Location = new Point(185, 301);
            passWord2.Name = "passWord2";
            passWord2.Size = new Size(203, 27);
            passWord2.TabIndex = 2;
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Location = new Point(125, 188);
            label2.Name = "label2";
            label2.Size = new Size(54, 20);
            label2.TabIndex = 3;
            label2.Text = "手机号";
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.Location = new Point(139, 264);
            label3.Name = "label3";
            label3.Size = new Size(39, 20);
            label3.TabIndex = 3;
            label3.Text = "密码";
            // 
            // label4
            // 
            label4.AutoSize = true;
            label4.Location = new Point(110, 304);
            label4.Name = "label4";
            label4.Size = new Size(69, 20);
            label4.TabIndex = 3;
            label4.Text = "确认密码";
            // 
            // parentName
            // 
            parentName.Location = new Point(185, 106);
            parentName.Name = "parentName";
            parentName.Size = new Size(203, 27);
            parentName.TabIndex = 2;
            // 
            // parentEmail
            // 
            parentEmail.Location = new Point(185, 224);
            parentEmail.Name = "parentEmail";
            parentEmail.Size = new Size(203, 27);
            parentEmail.TabIndex = 2;
            // 
            // label5
            // 
            label5.AutoSize = true;
            label5.Location = new Point(110, 109);
            label5.Name = "label5";
            label5.Size = new Size(69, 20);
            label5.TabIndex = 3;
            label5.Text = "家长姓名";
            // 
            // label6
            // 
            label6.AutoSize = true;
            label6.Location = new Point(139, 227);
            label6.Name = "label6";
            label6.Size = new Size(39, 20);
            label6.TabIndex = 3;
            label6.Text = "邮箱";
            // 
            // radioButton1
            // 
            radioButton1.AutoSize = true;
            radioButton1.Checked = true;
            radioButton1.Location = new Point(217, 149);
            radioButton1.Name = "radioButton1";
            radioButton1.Size = new Size(45, 24);
            radioButton1.TabIndex = 4;
            radioButton1.TabStop = true;
            radioButton1.Text = "男";
            radioButton1.UseVisualStyleBackColor = true;
            radioButton1.CheckedChanged += radioButton1_CheckedChanged;
            // 
            // radioButton2
            // 
            radioButton2.AutoSize = true;
            radioButton2.Location = new Point(302, 149);
            radioButton2.Name = "radioButton2";
            radioButton2.Size = new Size(45, 24);
            radioButton2.TabIndex = 4;
            radioButton2.TabStop = true;
            radioButton2.Text = "女";
            radioButton2.UseVisualStyleBackColor = true;
            radioButton2.CheckedChanged += radioButton2_CheckedChanged;
            // 
            // studentID
            // 
            studentID.Location = new Point(185, 344);
            studentID.Name = "studentID";
            studentID.Size = new Size(125, 27);
            studentID.TabIndex = 5;
            // 
            // label7
            // 
            label7.AutoSize = true;
            label7.Location = new Point(126, 347);
            label7.Name = "label7";
            label7.Size = new Size(54, 20);
            label7.TabIndex = 6;
            label7.Text = "学生ID";
            // 
            // Form3
            // 
            AutoScaleDimensions = new SizeF(9F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(571, 430);
            Controls.Add(label7);
            Controls.Add(studentID);
            Controls.Add(radioButton2);
            Controls.Add(radioButton1);
            Controls.Add(label4);
            Controls.Add(label6);
            Controls.Add(label3);
            Controls.Add(label5);
            Controls.Add(label2);
            Controls.Add(passWord2);
            Controls.Add(parentEmail);
            Controls.Add(passWord1);
            Controls.Add(parentName);
            Controls.Add(phoneNumber);
            Controls.Add(label1);
            Controls.Add(button2);
            Controls.Add(button1);
            FormBorderStyle = FormBorderStyle.FixedSingle;
            Name = "Form3";
            StartPosition = FormStartPosition.CenterScreen;
            Text = "注册";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Button button1;
        private Button button2;
        private Label label1;
        private TextBox phoneNumber;
        private TextBox passWord1;
        private TextBox passWord2;
        private Label label2;
        private Label label3;
        private Label label4;
        private TextBox parentName;
        private TextBox parentEmail;
        private Label label5;
        private Label label6;
        private RadioButton radioButton1;
        private RadioButton radioButton2;
        private TextBox studentID;
        private Label label7;
    }
}