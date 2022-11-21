import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddInterestDialogComponent } from './add-interest-dialog.component';

describe('AddInterestDialogComponent', () => {
  let component: AddInterestDialogComponent;
  let fixture: ComponentFixture<AddInterestDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AddInterestDialogComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AddInterestDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
