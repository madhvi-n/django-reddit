import { TestBed } from '@angular/core/testing';

import { StorageHandlerService } from './storage-handler.service';

describe('StorageHandlerService', () => {
  let service: StorageHandlerService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(StorageHandlerService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
