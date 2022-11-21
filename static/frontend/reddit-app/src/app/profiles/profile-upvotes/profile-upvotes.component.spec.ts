import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProfileUpvotesComponent } from './profile-upvotes.component';

describe('ProfileUpvotesComponent', () => {
  let component: ProfileUpvotesComponent;
  let fixture: ComponentFixture<ProfileUpvotesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProfileUpvotesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProfileUpvotesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
