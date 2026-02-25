export interface TimeControlOption {
    type: string;
    label: string;
    baseTime: string;       // total time for the game in minutes
    incrementPerMove: string;     // additional seconds added after each move
}

export const TIME_OPTIONS_MAP: { [key: string]: TimeControlOption[] } = {
    'bullet': [
        { type: 'bullet', label: '1 m', baseTime: '1', incrementPerMove: '0' },
        { type: 'bullet', label: '1 m | 1 s', baseTime: '1', incrementPerMove: '1' },
        { type: 'bullet', label: '2 m | 1 s', baseTime: '2', incrementPerMove: '1' }
    ],
    'blitz': [
        { type: 'blitz', label: '3 m', baseTime: '3', incrementPerMove: '0' },
        { type: 'blitz', label: '3 m | 2 s', baseTime: '3', incrementPerMove: '2' },
        { type: 'blitz', label: '5 m', baseTime: '5', incrementPerMove: '0' }
    ],
    'rapid': [
        { type: 'rapid', label: '10 m', baseTime: '10', incrementPerMove: '0' },
        { type: 'rapid', label: '15 m | 10 s', baseTime: '15', incrementPerMove: '10' },
        { type: 'rapid', label: '30 m', baseTime: '30', incrementPerMove: '0' }
    ]
};
