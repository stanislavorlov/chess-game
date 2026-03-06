import jwt from 'jsonwebtoken';

export const generateToken = (id: string): string => {
    const secret = process.env.JWT_SECRET || 'dev_secret_do_not_use_in_production';
    return jwt.sign({ id }, secret, {
        expiresIn: '30d',
    });
};
