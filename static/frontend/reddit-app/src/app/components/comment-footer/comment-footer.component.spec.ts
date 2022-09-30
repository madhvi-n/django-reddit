import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CommentFooterComponent } from './comment-footer.component';

describe('CommentFooterComponent', () => {
  let component: CommentFooterComponent;
  let fixture: ComponentFixture<CommentFooterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CommentFooterComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CommentFooterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
