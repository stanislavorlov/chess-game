import { TestBed } from '@angular/core/testing';

import { ChessService } from './chess.service';

import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';

describe('ChessService', () => {
  let service: ChessService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    });
    service = TestBed.inject(ChessService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
