import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SetttingsComponent } from './setttings.component';

describe('SetttingsComponent', () => {
  let component: SetttingsComponent;
  let fixture: ComponentFixture<SetttingsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SetttingsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SetttingsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
