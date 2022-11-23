import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PostLoaderComponent } from './post-loader.component';

describe('PostLoaderComponent', () => {
  let component: PostLoaderComponent;
  let fixture: ComponentFixture<PostLoaderComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PostLoaderComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PostLoaderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
