import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProfileDownvotesComponent } from './profile-downvotes.component';

describe('ProfileDownvotesComponent', () => {
  let component: ProfileDownvotesComponent;
  let fixture: ComponentFixture<ProfileDownvotesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProfileDownvotesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProfileDownvotesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
