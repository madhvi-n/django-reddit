import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProfileCommentsComponent } from './profile-comments.component';

describe('ProfileCommentsComponent', () => {
  let component: ProfileCommentsComponent;
  let fixture: ComponentFixture<ProfileCommentsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProfileCommentsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProfileCommentsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
