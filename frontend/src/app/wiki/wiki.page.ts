import {Component, inject, OnInit} from "@angular/core";

import {DataService} from "../services/data.service";
import {Platform} from "@ionic/angular";
import {
  ParsedDocumentTextTypes,
  ParsedQueryResponseDocument,
} from "../types/query-response.type";
import {ActivatedRoute} from "@angular/router";
import {ResponseParsingService} from "../services/response-parsing-service";

@Component({
  selector: "app-wiki",
  templateUrl: "./wiki.page.html",
  styleUrls: ["./wiki.page.scss"],
})
export class WikiPage implements OnInit {
  public docName: String;
  public wikiPage!: ParsedQueryResponseDocument;
  public createdHeaders: string[] = [];
  private data = inject(DataService);
  private activatedRoute = inject(ActivatedRoute);
  private platform = inject(Platform);

  constructor() {
  }

  ngOnInit() {
    this.docName = this.activatedRoute.snapshot.paramMap.get('id') as string;
    const idx = this.activatedRoute.snapshot.paramMap.get('id') as string;
    this.data.getDocomentById(parseInt(idx, 10)).then((res) => {
      this.wikiPage = ResponseParsingService.parseDocumentResponse(res);
    });
  }

  getBackButtonText() {
    const isIos = this.platform.is('ios')
    return isIos ? 'Inbox' : '';
  }

  addCreatedHeader(header: string) {
    this.createdHeaders.push(header);
  }

  isHeaderAlreadyCreated(header: string): boolean {
    return this.createdHeaders.includes(header);
  }

  protected readonly ParsedDocumentTextTypes = ParsedDocumentTextTypes;
}
