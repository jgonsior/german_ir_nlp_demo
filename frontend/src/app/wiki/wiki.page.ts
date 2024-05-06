import {Component, inject, OnInit} from "@angular/core";

import { DataService } from "../services/data.service";
import {Platform} from "@ionic/angular";
import {QueryResponseResult} from "../types/query-response.type";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: "app-wiki",
  templateUrl: "./wiki.page.html",
  styleUrls: ["./wiki.page.scss"],
})
export class WikiPage {
  public docname: String;
  public document!: String;
  public queryResult!: QueryResponseResult;
  private data = inject(DataService);
  private activatedRoute = inject(ActivatedRoute);
  private platform = inject(Platform);

  constructor() {}

  ngOnInit() {
    this.docname = this.activatedRoute.snapshot.paramMap.get('id') as string;
    const idx = this.activatedRoute.snapshot.paramMap.get('id') as string;
    this.queryResult = this.activatedRoute.snapshot.paramMap.get('answer') as unknown as QueryResponseResult;
    this.data.getDocomentById(parseInt(idx, 10)).then((res) => {
      this.document = res;
    });
  }

  getBackButtonText() {
    const isIos = this.platform.is('ios')
    return isIos ? 'Inbox' : '';
  }

}
