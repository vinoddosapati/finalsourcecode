import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewLatComponent } from './view-lat.component';

describe('ViewLatComponent', () => {
  let component: ViewLatComponent;
  let fixture: ComponentFixture<ViewLatComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ViewLatComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ViewLatComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
