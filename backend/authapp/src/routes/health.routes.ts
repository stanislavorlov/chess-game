import { Router, Request, Response } from 'express';
import mongoose from 'mongoose';

const router = Router();

router.get('/live', (req: Request, res: Response) => {
    res.json({ status: 'ok', service: 'authapp' });
});

router.get('/ready', (req: Request, res: Response) => {
    // 0 = disconnected, 1 = connected, 2 = connecting, 3 = disconnecting, 99 = uninitialized
    const dbStatus = mongoose.connection.readyState;

    if (dbStatus === 1) {
        res.status(200).json({
            status: 'ready',
            service: 'authapp',
            dbStatus: 'connected'
        });
    } else {
        res.status(503).json({
            status: 'not ready',
            service: 'authapp',
            dbStatus: 'disconnected'
        });
    }
});

export default router;
