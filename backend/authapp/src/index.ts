import express, { Request, Response } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { connectDB } from './config/db';
import authRoutes from './routes/auth.routes';

import path from 'path';

// Attempt to load from `../chessapp/.env` (if running via `npm run dev`) 
// or `../../chessapp/.env` (if running `node dist/index.js` inside the `authapp` folder)
const envPath = process.env.NODE_ENV === 'production'
    ? path.resolve(__dirname, '../../chessapp/.env')
    : path.resolve(__dirname, '../../chessapp/.env');

dotenv.config({ path: envPath });

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use('/api/auth', authRoutes);

app.get('/health', (req: Request, res: Response) => {
    res.json({ status: 'ok', service: 'authapp' });
});

const PORT = process.env.AUTH_PORT || 3000;

// Connect to MongoDB, then start server
connectDB().then(() => {
    app.listen(PORT, () => {
        console.log(`Auth Service running on port ${PORT}`);
    });
}).catch(err => {
    console.error('Failed to connect to MongoDB, starting server anyway for healthchecks', err);
    app.listen(PORT, () => {
        console.log(`Auth Service running on port ${PORT} (Disconnected from DB)`);
    });
});
