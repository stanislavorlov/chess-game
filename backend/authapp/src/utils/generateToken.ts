import jwt from 'jsonwebtoken';

export const generateToken = (id: string): string => {
    const secret = process.env.JWT_SECRET;
    if (!secret) {
        throw new Error('JWT_SECRET is not defined');
    }
    return jwt.sign({ sub: id, role: 'player' }, secret, {
        expiresIn: '15m',
        algorithm: 'HS256',
        issuer: 'chess-auth-app',
        audience: 'chess-app',
        jwtid: id,
    });
};

export const verifyToken = (token: string): string => {
    const secret = process.env.JWT_SECRET;
    if (!secret) {
        throw new Error('JWT_SECRET is not defined');
    }
    return jwt.verify(token, secret) as string;
};
