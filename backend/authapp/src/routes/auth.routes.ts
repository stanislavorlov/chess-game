import express, { Request, Response } from 'express';
import { Player } from '../models/Player';
import { generateToken } from '../utils/generateToken';

const router = express.Router();

// @desc    Register a new player
// @route   POST /api/auth/register
// @access  Public
router.post('/register', async (req: Request, res: Response): Promise<void> => {
    try {
        const { username, email, password } = req.body;

        const playerExists = await Player.findOne({ $or: [{ email }, { username }] });

        if (playerExists) {
            res.status(400).json({ message: 'Player with that username or email already exists' });
            return;
        }

        const player = await Player.create({
            username,
            email,
            passwordHash: password, // Mongoose pre-save hook will hash it
        });

        if (player) {
            res.status(201).json({
                _id: player._id,
                username: player.username,
                email: player.email,
                token: generateToken(player._id.toString()),
            });
        } else {
            res.status(400).json({ message: 'Invalid player data' });
        }
    } catch (error: any) {
        res.status(500).json({ message: error.message });
    }
});

// @desc    Auth user & get token
// @route   POST /api/auth/login
// @access  Public
router.post('/login', async (req: Request, res: Response): Promise<void> => {
    try {
        const { email, password } = req.body;

        // Note: We need to explicitly select passwordHash since we excluded it in the schema
        const player = await Player.findOne({ email }).select('+passwordHash');

        if (player && (await player.matchPassword(password))) {
            res.json({
                _id: player._id,
                username: player.username,
                email: player.email,
                token: generateToken(player._id.toString()),
            });
        } else {
            res.status(401).json({ message: 'Invalid email or password' });
        }
    } catch (error: any) {
        res.status(500).json({ message: error.message });
    }
});

export default router;
