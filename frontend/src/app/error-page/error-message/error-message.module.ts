import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';
import { FormsModule } from '@angular/forms';
import { ErrorMessageComponent } from './error-message.component';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
  ],
  declarations: [ErrorMessageComponent],
  exports: [ErrorMessageComponent]
})
export class ErrorMessageModule {}
