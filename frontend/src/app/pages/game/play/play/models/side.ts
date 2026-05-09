export class Side {
    private _value: string;

    constructor(value: string) {
        this._value = value;
    }

    public static white: Side = new Side('W');
    public static black: Side = new Side('B');

    get value(): string {
        return this._value;
    }

    get name(): string {
        return this._value === 'W' ? 'White' : 'Black';
    }

    static parse(value: string) {
        const upperValue = value.toUpperCase();
        if (upperValue == this.white.value)
            return Side.white;
        else if (upperValue == this.black.value)
            return Side.black;
        else {
            throw new Error('Un-supported Side value for parsing provided');
        }
    }
}