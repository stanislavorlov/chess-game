import { Document } from 'mongoose';

export interface IPlayer extends Document {
    username: string;
    email: string;
    passwordHash: string;
    level: number;
    firstName: string | null;
    lastName: string | null;
    country: string;
    createdAt: Date;
    matchPassword(enteredPassword: string): Promise<boolean>;
}