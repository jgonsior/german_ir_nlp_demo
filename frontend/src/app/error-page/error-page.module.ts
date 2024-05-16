import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';
import { FormsModule } from '@angular/forms';

import { ErrorPageComponent } from './error-page.component';
import { ErrorPageComponentRoutingModule } from './error-page-routing.module';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    ErrorPageComponentRoutingModule
  ],
  declarations: [ErrorPageComponent]
})
export class ErrorPageComponentModule {}
