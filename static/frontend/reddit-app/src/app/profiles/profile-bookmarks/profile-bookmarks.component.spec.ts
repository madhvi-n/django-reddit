import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProfileBookmarksComponent } from './profile-bookmarks.component';

describe('ProfileBookmarksComponent', () => {
  let component: ProfileBookmarksComponent;
  let fixture: ComponentFixture<ProfileBookmarksComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProfileBookmarksComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProfileBookmarksComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
