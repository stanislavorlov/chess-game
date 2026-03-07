import { Request, Response } from 'express';
import { Player } from '../schema/player.schema';
import { AuthRequest } from '../middlewares/auth.middleware';
import { PlayerRepository } from '../repository/player.repository';
import { mapPlayerToAuthResponse, mapPlayerToProfileResponse } from '../utils/dtoMapper';

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

        const player = await this.playerRepository.update(req.sub as string, {
            firstName: firstName ?? '',
            lastName: lastName ?? '',
            country: country ?? '',
            passwordHash: password ?? '',
        });

        if (!!player) {
            res.json(mapPlayerToProfileResponse(player));
        } else {
            res.status(401).json({ message: 'Player not found' });
        }
    }
}