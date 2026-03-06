import mongoose, { Schema } from "mongoose";
import bcrypt from 'bcryptjs';
import { IPlayer } from "../models/Player";

const PlayerSchema: Schema<IPlayer> = new Schema({
    username: {
        type: String,
        required: true,
        unique: true,
    },
    email: {
        type: String,
        required: true,
        unique: true,
        match: [
            /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/,
            'Please add a valid email'
        ]
    },
    passwordHash: {
        type: String,
        required: true,
        select: false // Do not return password hash by default
    },
    createdAt: {
        type: Date,
        default: Date.now,
    },
    level: {
        type: Number,
        required: true,
    },
    country: {
        type: String,
        required: true,
    },
    firstName: {
        type: String,
        required: false,
    },
    lastName: {
        type: String,
        required: false,
    }
});

// Method to verify passwords
PlayerSchema.methods.matchPassword = async function (enteredPassword: string) {
    return await bcrypt.compare(enteredPassword, this.passwordHash);
};

// Pre-save hook to hash password if it was modified
PlayerSchema.pre('save', async function (this: any) {
    if (!this.isModified('passwordHash')) {
        return;
    }

    const salt = await bcrypt.genSalt(10);
    this.passwordHash = await bcrypt.hash(this.passwordHash, salt);
});

export const Player = mongoose.model<IPlayer>('Player', PlayerSchema);