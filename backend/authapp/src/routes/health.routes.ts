import { Router, Request, Response } from 'express';
import mongoose from 'mongoose';
import { kafkaProducer } from '../index';

const router = Router();

router.get('/live', (req: Request, res: Response) => {
    res.json({ status: 'ok', service: 'authapp' });
});

router.get('/ready', (req: Request, res: Response) => {
    // 0 = disconnected, 1 = connected, 2 = connecting, 3 = disconnecting, 99 = uninitialized
    const dbStatus = mongoose.connection.readyState;
    const isDbConnected = dbStatus === 1;
    const isKafkaConnected = kafkaProducer.isConnected;

    if (isDbConnected && isKafkaConnected) {
        res.status(200).json({
            status: 'ready',
            service: 'authapp',
            dbStatus: 'connected',
            kafkaStatus: 'connected'
        });
    } else {
        res.status(503).json({
            status: 'not ready',
            service: 'authapp',
            dbStatus: isDbConnected ? 'connected' : 'disconnected',
            kafkaStatus: isKafkaConnected ? 'connected' : 'disconnected'
        });
    }
});

export default router;
