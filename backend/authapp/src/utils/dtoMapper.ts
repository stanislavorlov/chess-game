import { IPlayer } from "../models/Player";
import { generateToken } from "./generateToken";

export const mapPlayerToAuthResponse = (player: IPlayer) => {
    return {
        _id: player._id,
        username: player.username,
        email: player.email,
        level: player.level,
        country: player.country,
        token: generateToken(player._id.toString()),
    };
};

export const mapPlayerToProfileResponse = (player: IPlayer) => {
    return {
        _id: player._id,
        username: player.username,
        email: player.email,
        level: player.level,
        country: player.country ?? '',
        firstName: player.firstName ?? '',
        lastName: player.lastName ?? '',
    };
};
