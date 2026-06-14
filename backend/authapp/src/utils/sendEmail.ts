export const sendEmail = async (options: { email: string; subject: string; message: string }) => {
    // For development, we just log the email to the console.
    // In production, you would configure a transporter (e.g., using nodemailer, SendGrid, AWS SES)
    console.log(`\n================= MOCK EMAIL SENT =================`);
    console.log(`To: ${options.email}`);
    console.log(`Subject: ${options.subject}`);
    console.log(`Message:\n${options.message}`);
    console.log(`===================================================\n`);
};
