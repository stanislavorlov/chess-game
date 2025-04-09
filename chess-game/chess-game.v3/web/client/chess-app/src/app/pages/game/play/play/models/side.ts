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
}