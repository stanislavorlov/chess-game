import mongoose from 'mongoose';

export const connectDB = async () => {
    try {
        const mongoHost = process.env.MONGO_HOST;
        if (!mongoHost) {
            throw new Error('MONGO_HOST is not defined in environment variables');
        }

        const conn = await mongoose.connect(mongoHost, {
            // Options are largely deprecated in mongoose 6+ as they resolve automatically
        });

        console.log(`MongoDB Connected: ${conn.connection.host}`);
    } catch (error: any) {
        console.error(`MongoDB connection error: ${error.message}`);
        process.exit(1);
    }
};
