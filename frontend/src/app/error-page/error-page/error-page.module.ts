import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';
import { FormsModule } from '@angular/forms';
import { ErrorPageComponent } from './error-page.component';
import { ErrorPageRoutingModule } from './error-page-routing.module';
import { ErrorMessageModule } from '../error-message/error-message.module';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    ErrorMessageModule,
    ErrorPageRoutingModule,
  ],
  declarations: [ErrorPageComponent],
  exports: [ErrorPageComponent]
})
export class ErrorPageModule {}
