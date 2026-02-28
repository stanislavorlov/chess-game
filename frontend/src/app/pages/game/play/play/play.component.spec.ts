import { ComponentFixture, TestBed } from '@angular/core/testing';
import { PlayComponent } from './play.component';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { ActivatedRoute } from '@angular/router';
import { of } from 'rxjs';
import { ChessService } from 'src/app/services/chess.service';
import { SanMovement, SquareMovement } from 'src/app/services/models/movement';
import { By } from '@angular/platform-browser';
import { PlayService } from 'src/app/services/play.service';

describe('PlayComponent', () => {
  let component: PlayComponent;
  let fixture: ComponentFixture<PlayComponent>;
  let chessServiceSpy: jasmine.SpyObj<ChessService>;
  let playServiceSpy: jasmine.SpyObj<PlayService>;

  const mockGameDto = {
    game_id: '507f191e810c19729de860ea',
    name: 'Test Game',
    game_format: {
      value: 'standard',
      white_remaining_time: 600,
      black_remaining_time: 600,
      move_increment: 0
    },
    state: {
      turn: 'W',
      started: true,
      finished: false,
      check_side: null,
      check_position: null,
      legal_moves: 'e2e4 e7e5'
    },
    board: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR',
    history: 'e4,e5,Nf3'
  };

  beforeEach(async () => {
    chessServiceSpy = jasmine.createSpyObj('ChessService', ['getGame', 'newGame', 'startGame']);
    playServiceSpy = jasmine.createSpyObj('PlayService', ['setGameId', 'sendMessage', 'getMessages', 'closeConnection']);
    playServiceSpy.getMessages.and.returnValue(of());
    chessServiceSpy.getGame.and.returnValue(of(mockGameDto as any));

    await TestBed.configureTestingModule({
      imports: [PlayComponent, NoopAnimationsModule],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        { provide: ChessService, useValue: chessServiceSpy },
        { provide: PlayService, useValue: playServiceSpy },
        {
          provide: ActivatedRoute,
          useValue: {
            snapshot: {
              paramMap: {
                get: (key: string) => (key === 'id' ? '507f191e810c19729de860ea' : null)
              }
            },
            params: of({ id: '507f191e810c19729de860ea' }),
            queryParams: of({})
          }
        }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(PlayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load history as SanMovement objects', () => {
    expect(component.game.history.length).toBe(3);
    expect(component.game.history[0]).toBeInstanceOf(SanMovement);
    expect((component.game.history[0] as SanMovement).san).toBe('e4');
    expect(component.game.history[0].displayValue).toBe('e4');
  });

  it('should create SquareMovement when a move is made', () => {
    // Initial history length is 3 from mock
    const initialHistoryLength = component.game.history.length;

    // Simulate clicking e2 then e4
    const e2 = component.game.board.getCell('e2')!;
    const e4 = component.game.board.getCell('e4')!;

    // Select e2
    component.clickBoard(e2);
    expect(e2.selected).toBeTrue();

    // Move to e4
    component.clickBoard(e4);

    expect(component.game.history.length).toBe(initialHistoryLength + 1);
    const lastMove = component.game.history[component.game.history.length - 1];
    expect(lastMove).toBeInstanceOf(SquareMovement);
    expect((lastMove as SquareMovement).from).toBe('e2');
    expect((lastMove as SquareMovement).to).toBe('e4');
    expect(lastMove.displayValue).toBe('e2-e4');
  });

  it('should display move displayValue in history list', () => {
    fixture.detectChanges();
    const historyItems = fixture.debugElement.queryAll(By.css('.history-item span'));

    expect(historyItems.length).toBe(3);
    expect(historyItems[0].nativeElement.textContent).toContain('e4');
    expect(historyItems[1].nativeElement.textContent).toContain('e5');
    expect(historyItems[2].nativeElement.textContent).toContain('Nf3');

    // Add a square move and check display
    const e2 = component.game.board.getCell('e2')!;
    const e4 = component.game.board.getCell('e4')!;
    const initialHistoryLength = component.game.history.length;
    component.clickBoard(e2);
    component.clickBoard(e4);

    fixture.detectChanges();
    const updatedHistoryItems = fixture.debugElement.queryAll(By.css('.history-item span'));
    expect(updatedHistoryItems.length).toBe(initialHistoryLength + 1);
  });
});
