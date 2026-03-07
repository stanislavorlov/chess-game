import { Player } from "../schema/player.schema";
import { IPlayer } from "../models/Player";

export class PlayerRepository {
    async create(playerData: Partial<IPlayer>): Promise<IPlayer> {
        const player = new Player(playerData);
        return await player.save();
    }

    async findByEmail(email: string, includePassword = false): Promise<IPlayer | null> {
        let query = Player.findOne({ email });
        if (includePassword) {
            query = query.select('+passwordHash');
        }
        return query;
    }

    async findById(id: string): Promise<IPlayer | null> {
        return Player.findById(id).select('-passwordHash');
    }

    async update(id: string, playerData: Partial<IPlayer>): Promise<IPlayer | null> {
        return Player.findByIdAndUpdate(id, playerData, { new: true }).select('-passwordHash');
    }
}