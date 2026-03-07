import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import path from 'path';
import { connectDB } from './config/db';
import { setupSwagger } from './config/swagger';
import authRoutes from './routes/auth.routes';
import healthRoutes from './routes/health.routes';
import { KafkaProducer } from './kafka/producer';

// Attempt to load from `../chessapp/.env` (if running via `npm run dev`) 
// or `../../chessapp/.env` (if running `node dist/index.js` inside the `authapp` folder)
const envPath = process.env.NODE_ENV === 'production'
    ? path.resolve(__dirname, '../../authapp/.env')
    : path.resolve(__dirname, '../../authapp/.env');

dotenv.config({ path: envPath });

const kafkaBroker = process.env.KAFKA_BROKER || 'localhost:9092';
const kafkaClientId = process.env.KAFKA_CLIENT_ID || 'authapp-producer';

export const kafkaProducer = new KafkaProducer({
    broker: kafkaBroker,
    clientId: kafkaClientId
});

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Swagger
setupSwagger(app);

// Routes
app.use('/health', healthRoutes);
app.use('/api/auth', authRoutes);

const PORT = process.env.AUTH_PORT || 3000;

// Connect to MongoDB and Kafka, then start server
Promise.allSettled([connectDB(), kafkaProducer.connect()]).then((results) => {
    const [dbResult, kafkaResult] = results;

    if (dbResult.status === 'rejected') {
        console.error('Failed to connect to MongoDB, starting server anyway for healthchecks', dbResult.reason);
    }
    if (kafkaResult.status === 'rejected') {
        console.error('Failed to connect to Kafka, continuing anyway', kafkaResult.reason);
    }

    app.listen(PORT, () => {
        const dbStatus = dbResult.status === 'fulfilled' ? '(Connected to DB)' : '(Disconnected from DB)';
        console.log(`Auth Service running on port ${PORT} ${dbStatus}`);
    });
});

const gracefulShutdown = async () => {
    console.log('Shutting down gracefully...');
    try {
        await kafkaProducer.disconnect();
    } catch (err) {
        console.error('Error during Kafka disconnect', err);
    }
    process.exit(0);
};

process.on('SIGINT', gracefulShutdown);
process.on('SIGTERM', gracefulShutdown);
