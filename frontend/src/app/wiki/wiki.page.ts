import {Component, inject, OnInit} from "@angular/core";

import { DataService, Message} from "../services/data.service";
import {RefresherCustomEvent} from "@ionic/angular";

@Component({
  selector: "app-wiki",
  templateUrl: "./wiki.page.html",
  styleUrls: ["./wiki.page.scss"],
})
export class WikiPage {
  private data: DataService = inject(DataService);
  //protected queryResults: QueryResponseResult[] = [];

  constructor(private dataService: DataService) {}

  refresh(ev: any) {
    setTimeout(() => {
      (ev as RefresherCustomEvent).detail.complete();
    }, 3000)
  }

  getMessages(): Message[] {
    return this.data.getMessages()
  }

}
