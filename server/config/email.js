// Email Configuration
const nodemailer = require("nodemailer");

// For testing/development - Use Ethereal.email (fake SMTP)
// Get free test account at: https://ethereal.email/
const config = {
  host: process.env.EMAIL_HOST || "smtp.ethereal.email",
  port: process.env.EMAIL_PORT || 587,
  secure: process.env.EMAIL_SECURE === "true", // true for 465, false for other ports
  auth: {
    user: process.env.EMAIL_USER || "lucile.steuber@ethereal.email",
    pass: process.env.EMAIL_PASS || "8xfWYrSQb13yCK77nH",
  },
};

// Create transporter
const transporter = nodemailer.createTransport(config);

// Test email configuration
async function testEmailConfig() {
  try {
    const testAccount = await nodemailer.createTestAccount();
    console.log(" Test email account created:");
    console.log("  Email:", testAccount.user);
    console.log("  Pass:", testAccount.pass);
    console.log("  Web: https://ethereal.email");
    return true;
  } catch (error) {
    console.error("Email config error:", error.message);
    return false;
  }
}

// Send email function
async function sendEmail(to, subject, htmlContent) {
  try {
    const info = await transporter.sendMail({
      from: `"Hospital Management System" <${config.auth.user}>`,
      to: to,
      subject: subject,
      html: htmlContent,
    });

    console.log(` Email sent to ${to}: ${info.messageId}`);
    
    // Preview URL for Ethereal emails
    if (config.host.includes("ethereal.email")) {
      console.log(`  Preview: ${nodemailer.getTestMessageUrl(info)}`);
    }
    
    return { success: true, messageId: info.messageId };
  } catch (error) {
    console.error(" Email sending failed:", error.message);
    return { success: false, error: error.message };
  }
}

module.exports = {
  transporter,
  sendEmail,
  testEmailConfig,
  config,
};
