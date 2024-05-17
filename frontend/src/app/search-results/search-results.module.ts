import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { SearchResultsPageRoutingModule } from './search-results-routing.module';
import { MessageComponentModule } from '../message/message.module';
import { ErrorMessageModule } from '../error-page/error-message/error-message.module';

import { SearchResultsPage } from './search-results.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    ErrorMessageModule,
    MessageComponentModule,
    SearchResultsPageRoutingModule
  ],
  declarations: [SearchResultsPage]
})
export class SearchResultsPageModule {}
