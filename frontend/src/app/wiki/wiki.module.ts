import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';
import { FormsModule } from '@angular/forms';

import { WikiPage } from './wiki.page';
import { WikiPageRoutingModule } from './wiki-routing.module';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    WikiPageRoutingModule
  ],
  declarations: [WikiPage]
})
export class WikiPageModule {}
