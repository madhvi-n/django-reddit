import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GroupFeedComponent } from './group-feed.component';

describe('GroupFeedComponent', () => {
  let component: GroupFeedComponent;
  let fixture: ComponentFixture<GroupFeedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GroupFeedComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GroupFeedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
