import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { SearchResultsPageRoutingModule } from './search-results-routing.module';
import { ErrorMessageModule } from '../error-page/error-message/error-message.module';

import { SearchResultsPage } from './search-results.page';
import {SearchAnswerComponentModule} from "../search-answer/search-answer.module";

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    SearchResultsPageRoutingModule,
    SearchAnswerComponentModule,
    ErrorMessageModule,
    SearchResultsPageRoutingModule
  ],
  declarations: [SearchResultsPage]
})
export class SearchResultsPageModule {}
