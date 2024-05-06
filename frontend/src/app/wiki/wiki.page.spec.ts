import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterModule } from '@angular/router';
import { IonicModule } from '@ionic/angular';

import { WikiPage } from "./wiki.page";
import {WikiPageRoutingModule} from "./wiki-routing.module";

describe('WikiPage', () => {
  let component: WikiPage;
  let fixture: ComponentFixture<WikiPage>;

  beforeEach(async () => {
    TestBed.configureTestingModule({
      declarations: [WikiPage],
      imports: [IonicModule.forRoot(), WikiPageRoutingModule, RouterModule.forRoot([])],
    }).compileComponents();

    fixture = TestBed.createComponent(WikiPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  })
});
