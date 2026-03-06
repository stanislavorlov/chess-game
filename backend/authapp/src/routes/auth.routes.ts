import express, { Request, Response } from 'express';
import { generateToken } from '../utils/generateToken';
import { Player } from '../schema/player.schema';

const router = express.Router();

/**
 * @swagger
 * /api/auth/register:
 *   post:
 *     summary: Register a new player
 *     tags: [Auth]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - username
 *               - email
 *               - password
 *               - level
 *               - country
 *             properties:
 *               username:
 *                 type: string
 *               email:
 *                 type: string
 *               password:
 *                 type: string
 *               level:
 *                 type: integer
 *               country:
 *                 type: string
 *     responses:
 *       201:
 *         description: Player registered successfully
 *       400:
 *         description: Bad request (user exists or invalid data)
 *       500:
 *         description: Server error
 */
// @desc    Register a new player
// @route   POST /api/auth/register
// @access  Public
router.post('/register', async (req: Request, res: Response): Promise<void> => {
    try {
        const { username, email, password, level, country } = req.body;

        const playerExists = await Player.findOne({ $or: [{ email }, { username }] });

        if (playerExists) {
            res.status(400).json({ message: 'Player with that username or email already exists' });
            return;
        }

        const player = await Player.create({
            username,
            email,
            passwordHash: password, // Mongoose pre-save hook will hash it
            level,
            country
        });

        if (player) {
            res.status(201).json({
                _id: player._id,
                username: player.username,
                email: player.email,
                token: generateToken(player._id.toString()),
                level: player.level,
                country: player.country
            });
        } else {
            res.status(400).json({ message: 'Invalid player data' });
        }
    } catch (error: any) {
        res.status(500).json({ message: error.message });
    }
});

/**
 * @swagger
 * /api/auth/login:
 *   post:
 *     summary: Authenticate a player and get token
 *     tags: [Auth]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - email
 *               - password
 *             properties:
 *               email:
 *                 type: string
 *               password:
 *                 type: string
 *     responses:
 *       200:
 *         description: Login successful
 *       401:
 *         description: Invalid email or password
 *       500:
 *         description: Server error
 */
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
                level: player.level,
                country: player.country
            });
        } else {
            res.status(401).json({ message: 'Invalid email or password' });
        }
    } catch (error: any) {
        res.status(500).json({ message: error.message });
    }
});

export default router;
