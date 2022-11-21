import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GroupRouterComponent } from './group-router.component';

describe('GroupRouterComponent', () => {
  let component: GroupRouterComponent;
  let fixture: ComponentFixture<GroupRouterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GroupRouterComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GroupRouterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
