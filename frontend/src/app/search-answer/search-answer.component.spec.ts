import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterModule } from '@angular/router';
import { IonicModule } from '@ionic/angular';

import { SearchAnswerComponent } from './search-answer.component';

describe('MessageComponent', () => {
  let component: SearchAnswerComponent;
  let fixture: ComponentFixture<SearchAnswerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SearchAnswerComponent],
      imports: [IonicModule.forRoot(), RouterModule.forRoot([])]
    }).compileComponents();

    fixture = TestBed.createComponent(SearchAnswerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
