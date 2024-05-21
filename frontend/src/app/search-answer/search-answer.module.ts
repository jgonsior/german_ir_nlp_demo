import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

import { IonicModule } from '@ionic/angular';

import { SearchAnswerComponent } from './search-answer.component';

@NgModule({
  imports: [ CommonModule, FormsModule, IonicModule, RouterModule],
  declarations: [SearchAnswerComponent],
  exports: [SearchAnswerComponent]
})
export class SearchAnswerComponentModule {}
