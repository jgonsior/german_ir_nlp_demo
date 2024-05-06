import {Component, inject, OnInit} from "@angular/core";

import { DataService } from "../services/data.service";
import {Platform} from "@ionic/angular";
import {QueryResponseResult, QueryResponseDocument, QueryResponsePage} from "../types/query-response.type";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: "app-wiki",
  templateUrl: "./wiki.page.html",
  styleUrls: ["./wiki.page.scss"],
})
export class WikiPage {
  public doc_name: String;
  public document: QueryResponsePage;
  public passages: QueryResponseDocument;
  public queryResult!: QueryResponseResult;
  private data = inject(DataService);
  private activatedRoute = inject(ActivatedRoute);
  private platform = inject(Platform);

  constructor() {}

  ngOnInit() {
    this.doc_name = this.activatedRoute.snapshot.paramMap.get('id') as string;
    const idx = this.activatedRoute.snapshot.paramMap.get('id') as string;
    this.queryResult = this.activatedRoute.snapshot.paramMap.get('answer') as unknown as QueryResponseResult;
    this.data.getDocomentById(parseInt(idx, 10)).then((res) => {
      this.document = res as unknown as QueryResponsePage;
    });
    let page = this.document.page
    this.passages = page as unknown as QueryResponseDocument;
  }

  getBackButtonText() {
    const isIos = this.platform.is('ios')
    return isIos ? 'Inbox' : '';
  }

}
