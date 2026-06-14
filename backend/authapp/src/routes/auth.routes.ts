import express, { Request, Response } from 'express';
import { AuthController } from '../controllers/auth.controller';
import { PlayerRepository } from '../repository/player.repository';
import { authMiddleware, AuthRequest } from '../middlewares/auth.middleware';

const router = express.Router();
const playerRepository = new PlayerRepository();
const authController = new AuthController(playerRepository);

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
        await authController.registerUser(req, res);
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
        await authController.loginUser(req, res);
    } catch (error: any) {
        res.status(500).json({ message: error.message });
    }
});

router.get('/health', (req: Request, res: Response): void => {
    res.json({ status: 'ok', service: 'authapp' });
});

/**
 * @swagger
 * /api/auth/currentPlayer:
 *   get:
 *     summary: Get current player
 *     tags: [Auth]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Current player
 *       401:
 *         description: Not authorized
 *       500:
 *         description: Server error
 */
// @desc    Get current player
// @route   GET /api/auth/currentPlayer
// @access  Private
router.get('/currentPlayer', authMiddleware, async (req: AuthRequest, res: Response): Promise<void> => {
    try {
        await authController.getProfile(req, res);
    } catch (error: any) {
        console.log(error);
        res.status(401).json({ message: 'Not authorized, token failed' });
    }
});

/**
 * @swagger
 * /api/auth/updatePlayer:
 *   post:
 *     summary: Update current player
 *     tags: [Auth]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               firstName:
 *                 type: string
 *               lastName:
 *                 type: string
 *               country:
 *                 type: string
 *               password:
 *                 type: string
 *     responses:
 *       200:
 *         description: Player updated successfully
 *       401:
 *         description: Not authorized
 *       500:
 *         description: Server error
 */
// @desc    Update current player
// @route   POST /api/auth/updatePlayer
// @access  Private
router.post('/updatePlayer', authMiddleware, async (req: AuthRequest, res: Response): Promise<void> => {
    try {
        await authController.updateProfile(req, res);
    } catch (error: any) {
        res.status(500).json({ message: error.message });
    }
});

/**
 * @swagger
 * /api/auth/forgotPassword:
 *   post:
 *     summary: Forgot Password
 *     tags: [Auth]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - email
 *             properties:
 *               email:
 *                 type: string
 *     responses:
 *       200:
 *         description: Email sent
 *       404:
 *         description: There is no user with that email
 *       500:
 *         description: Email could not be sent
 */
// @desc    Forgot Password
// @route   POST /api/auth/forgotPassword
// @access  Public
router.post('/forgotPassword', async (req: Request, res: Response): Promise<void> => {
    try {
        await authController.forgotPassword(req, res);
    } catch (error: any) {
        res.status(500).json({ message: error.message });
    }
});

/**
 * @swagger
 * /api/auth/resetPassword/{token}:
 *   post:
 *     summary: Reset Password
 *     tags: [Auth]
 *     parameters:
 *       - in: path
 *         name: token
 *         required: true
 *         schema:
 *           type: string
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - password
 *             properties:
 *               password:
 *                 type: string
 *     responses:
 *       200:
 *         description: Password updated successfully
 *       400:
 *         description: Invalid token
 *       500:
 *         description: Server error
 */
// @desc    Reset Password
// @route   POST /api/auth/resetPassword/:token
// @access  Public
router.post('/resetPassword/:token', async (req: Request, res: Response): Promise<void> => {
    try {
        await authController.resetPassword(req, res);
    } catch (error: any) {
        res.status(500).json({ message: error.message });
    }
});

export default router;
