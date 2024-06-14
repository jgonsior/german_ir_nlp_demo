import {importProvidersFrom, NgModule} from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouteReuseStrategy } from '@angular/router';

import { IonicModule, IonicRouteStrategy } from '@ionic/angular';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import {HttpClientModule, provideHttpClient} from "@angular/common/http";
import {simpleHttpInterceptorProvider} from "./services/simple-http-interceptor";

@NgModule({
  declarations: [AppComponent],
  imports: [BrowserModule, IonicModule.forRoot(), AppRoutingModule],
  providers: [{ provide: RouteReuseStrategy, useClass: IonicRouteStrategy }, importProvidersFrom(HttpClientModule), simpleHttpInterceptorProvider],
  bootstrap: [AppComponent],
})
export class AppModule {}
