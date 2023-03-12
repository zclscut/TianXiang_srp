namespace 在线学习状态分析系统家长端
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
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
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            label1 = new Label();
            label2 = new Label();
            label3 = new Label();
            label4 = new Label();
            phoneNumber = new TextBox();
            passWord = new TextBox();
            linkLabel1 = new LinkLabel();
            button1 = new Button();
            SuspendLayout();
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("Microsoft YaHei UI", 28F, FontStyle.Regular, GraphicsUnit.Point);
            label1.Location = new Point(36, 9);
            label1.Name = "label1";
            label1.Size = new Size(495, 60);
            label1.TabIndex = 0;
            label1.Text = "在线学习状态分析系统";
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Location = new Point(127, 140);
            label2.Name = "label2";
            label2.Size = new Size(54, 20);
            label2.TabIndex = 1;
            label2.Text = "手机号";
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.Location = new Point(142, 209);
            label3.Name = "label3";
            label3.Size = new Size(39, 20);
            label3.TabIndex = 2;
            label3.Text = "密码";
            // 
            // label4
            // 
            label4.AutoSize = true;
            label4.Font = new Font("Microsoft YaHei UI", 12F, FontStyle.Regular, GraphicsUnit.Point);
            label4.Location = new Point(245, 78);
            label4.Name = "label4";
            label4.Size = new Size(72, 27);
            label4.TabIndex = 3;
            label4.Text = "家长端";
            // 
            // phoneNumber
            // 
            phoneNumber.Location = new Point(187, 137);
            phoneNumber.Name = "phoneNumber";
            phoneNumber.Size = new Size(189, 27);
            phoneNumber.TabIndex = 4;
            // 
            // passWord
            // 
            passWord.Location = new Point(187, 202);
            passWord.Name = "passWord";
            passWord.Size = new Size(188, 27);
            passWord.TabIndex = 5;
            // 
            // linkLabel1
            // 
            linkLabel1.AutoSize = true;
            linkLabel1.Location = new Point(394, 140);
            linkLabel1.Name = "linkLabel1";
            linkLabel1.Size = new Size(39, 20);
            linkLabel1.TabIndex = 6;
            linkLabel1.TabStop = true;
            linkLabel1.Text = "注册";
            linkLabel1.LinkClicked += linkLabel1_LinkClicked;
            // 
            // button1
            // 
            button1.Location = new Point(234, 283);
            button1.Name = "button1";
            button1.Size = new Size(94, 29);
            button1.TabIndex = 8;
            button1.Text = "登录";
            button1.UseVisualStyleBackColor = true;
            button1.Click += button1_Click;
            // 
            // Form1
            // 
            ClientSize = new Size(571, 397);
            Controls.Add(button1);
            Controls.Add(linkLabel1);
            Controls.Add(passWord);
            Controls.Add(phoneNumber);
            Controls.Add(label4);
            Controls.Add(label3);
            Controls.Add(label2);
            Controls.Add(label1);
            FormBorderStyle = FormBorderStyle.FixedSingle;
            Name = "Form1";
            StartPosition = FormStartPosition.CenterScreen;
            Text = "在线学习状态分析系统（家长端）";
            Load += Form1_Load_1;
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Label label1;
        private Label label2;
        private Label label3;
        private Label label4;
        private TextBox phoneNumber;
        private TextBox passWord;
        private LinkLabel linkLabel1;
        private Button button1;
    }
}