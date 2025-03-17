export interface Position {
    square: string;
    piece: string;
    color: string;
  }
  export interface GroupedPosition {
    key: string;
    group: Position[];
  }