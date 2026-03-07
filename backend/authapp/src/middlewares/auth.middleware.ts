import { NextFunction, Request, Response } from "express";
import { verifyToken } from "../utils/generateToken";

export interface AuthRequest extends Request {
    sub?: string;
}

export const authMiddleware = (req: AuthRequest, res: Response, next: NextFunction) => {
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        res.status(401).json({ message: 'Not authorized' });
        return;
    }

    const token = authHeader.split(' ')[1];

    try {
        const decodedToken = verifyToken(token);
        if (!decodedToken) {
            res.status(401).json({ message: 'Not authorized' });
            return;
        }

        if (typeof decodedToken === 'string') {
            req.sub = decodedToken;
        } else if (decodedToken.sub) {
            req.sub = decodedToken.sub;
        }
        next();
    } catch (error) {
        res.status(401).json({ message: 'Not authorized, token failed' });
    }
}