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

    static parse(value: string) {
        if (value == this.white.value)
            return Side.white;
        else if (value == this.black.value)
            return Side.black;
        else {
            throw new Error('Un-supported Side value for parsing provided');
        }
    }
}