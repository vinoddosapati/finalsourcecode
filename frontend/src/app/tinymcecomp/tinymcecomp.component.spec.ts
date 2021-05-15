import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TinymcecompComponent } from './tinymcecomp.component';

describe('TinymcecompComponent', () => {
  let component: TinymcecompComponent;
  let fixture: ComponentFixture<TinymcecompComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TinymcecompComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TinymcecompComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
