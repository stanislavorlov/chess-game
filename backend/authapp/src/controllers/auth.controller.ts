import { Request, Response } from 'express';
import crypto from 'crypto';
import { Player } from '../schema/player.schema';
import { AuthRequest } from '../middlewares/auth.middleware';
import { PlayerRepository } from '../repository/player.repository';
import { mapPlayerToAuthResponse, mapPlayerToProfileResponse } from '../utils/dtoMapper';
import { sendEmail } from '../utils/sendEmail';

export class AuthController {
    constructor(private playerRepository: PlayerRepository) { }

    registerUser = async (req: Request, res: Response): Promise<void> => {
        const { username, email, password } = req.body;

        const playerExists = await Player.findOne({ $or: [{ email }, { username }] });

        if (playerExists) {
            res.status(400).json({ message: 'Player with that username or email already exists' });
            return;
        }

        const player = await this.playerRepository.create({
            ...req.body,
            passwordHash: password, // Mongoose pre-save hook will hash it
        });

        if (player) {
            res.status(201).json(mapPlayerToAuthResponse(player));
        } else {
            res.status(400).json({ message: 'Invalid player data' });
        }
    }

    loginUser = async (req: Request, res: Response): Promise<void> => {
        const { email, password } = req.body;

        const player = await this.playerRepository.findByEmail(email, true);

        if (player && (await player.matchPassword(password))) {
            res.json(mapPlayerToAuthResponse(player));
        } else {
            res.status(401).json({ message: 'Invalid email or password' });
        }
    }

    getProfile = async (req: AuthRequest, res: Response): Promise<void> => {
        const player = await this.playerRepository.findById(req.sub as string);

        if (!!player) {
            res.json(mapPlayerToProfileResponse(player));
        } else {
            res.status(401).json({ message: 'Player not found' });
        }
    }

    updateProfile = async (req: AuthRequest, res: Response): Promise<void> => {
        const { firstName, lastName, country, password } = req.body;

        const updateData: any = {
            firstName: firstName ?? '',
            lastName: lastName ?? '',
            country: country ?? '',
        };

        if (password) {
            updateData.passwordHash = password;
        }

        const player = await this.playerRepository.update(req.sub as string, updateData);

        if (!!player) {
            res.json(mapPlayerToProfileResponse(player));
        } else {
            res.status(401).json({ message: 'Player not found' });
        }
    }

    forgotPassword = async (req: Request, res: Response): Promise<void> => {
        const { email } = req.body;

        const player = await this.playerRepository.findByEmail(email);

        if (!player) {
            res.status(404).json({ message: 'There is no user with that email' });
            return;
        }

        const resetToken = crypto.randomBytes(20).toString('hex');

        // Hash token and set to resetPasswordToken field
        player.resetPasswordToken = crypto.createHash('sha256').update(resetToken).digest('hex');
        player.resetPasswordExpire = new Date(Date.now() + 10 * 60 * 1000); // 10 minutes

        await player.save();

        const resetUrl = `http://localhost:4200/authentication/reset-password/${resetToken}`;

        const message = `You are receiving this email because you (or someone else) has requested the reset of a password. Please go to this link to reset your password: \n\n ${resetUrl}`;

        try {
            await sendEmail({
                email: player.email,
                subject: 'Password reset token',
                message,
            });

            res.status(200).json({ success: true, data: 'Email sent' });
        } catch (err) {
            player.resetPasswordToken = undefined;
            player.resetPasswordExpire = undefined;
            await player.save();

            res.status(500).json({ message: 'Email could not be sent' });
        }
    }

    resetPassword = async (req: Request, res: Response): Promise<void> => {
        const resetPasswordToken = crypto.createHash('sha256').update(req.params.token as string).digest('hex');

        const player = await this.playerRepository.findByResetToken(resetPasswordToken);

        if (!player) {
            res.status(400).json({ message: 'Invalid token' });
            return;
        }

        player.passwordHash = req.body.password;
        player.resetPasswordToken = undefined;
        player.resetPasswordExpire = undefined;

        await player.save();

        res.status(200).json({ success: true, data: 'Password updated successfully' });
    }
}