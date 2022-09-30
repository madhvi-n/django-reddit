import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CommentUserComponent } from './comment-user.component';

describe('CommentUserComponent', () => {
  let component: CommentUserComponent;
  let fixture: ComponentFixture<CommentUserComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CommentUserComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CommentUserComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
