import { Component, inject } from '@angular/core';
import { RefresherCustomEvent } from '@ionic/angular';
import { MessageComponent } from '../message/message.component';

import { DataService } from '../services/data.service';
import {QueryResponseResult} from "../types/query-response.type";

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {
  private data = inject(DataService);
  protected queryResults: QueryResponseResult[] = [];
  constructor() {
    this.getMessages()
  }

  refresh(ev: any) {
    setTimeout(() => {
      (ev as RefresherCustomEvent).detail.complete();
    }, 3000);
  }

  async getMessages() {
    await this.data.getQueryResults('Harry').then((response) => {
      this.queryResults = response;
    });
  }
}
