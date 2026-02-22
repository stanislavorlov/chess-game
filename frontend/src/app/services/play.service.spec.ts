import { TestBed } from '@angular/core/testing';

import { PlayService } from './play.service';

import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';

describe('PlayService', () => {
  let service: PlayService;

  beforeEach(() => {
    service = new PlayService('test-game-id');
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
