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
export class WikiPage implements OnInit{
  public doc_name: String;
  public document: QueryResponsePage;
  public queryResult!: QueryResponseResult;
  public sorted_doc: Map<string[], string[]> = new Map();
  private data = inject(DataService);
  private activatedRoute = inject(ActivatedRoute);
  private platform = inject(Platform);

  constructor() {}

  ngOnInit() {
    this.doc_name = this.activatedRoute.snapshot.paramMap.get('id') as string;
    const idx = this.activatedRoute.snapshot.paramMap.get('id') as string;
    this.queryResult = this.activatedRoute.snapshot.paramMap.get('answer') as unknown as QueryResponseResult;
    this.data.getDocomentById(parseInt(idx, 10)).then((res) => {
      this.document = res;
      console.log(this.document)
    });

    let current_head: string[] = [];
    let passages: string[] = [];

    for (let page of this.document.page) {
      if (current_head == page.headers) {
        passages.push(page.passage);
      }
      else {
        this.sorted_doc.set(current_head,passages);
        current_head = page.headers;
        passages = [];
        passages.push(page.passage);
      }
    }

  }

  getBackButtonText() {
    const isIos = this.platform.is('ios')
    return isIos ? 'Inbox' : '';
  }

}
