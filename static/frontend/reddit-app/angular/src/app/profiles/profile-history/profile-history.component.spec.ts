import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProfileHistoryComponent } from './profile-history.component';

describe('ProfileHistoryComponent', () => {
  let component: ProfileHistoryComponent;
  let fixture: ComponentFixture<ProfileHistoryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProfileHistoryComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProfileHistoryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
