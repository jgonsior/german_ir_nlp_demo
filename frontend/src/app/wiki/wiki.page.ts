import {Component, inject, OnInit} from "@angular/core";

import {DataService} from "../services/data.service";
import {Platform} from "@ionic/angular";
import {
  ParsedDocumentTextTypes,
  ParsedQueryResponseDocument,
} from "../types/query-response.type";
import {ActivatedRoute, Router} from "@angular/router";
import {ResponseParsingService} from "../services/response-parsing-service";
import {DataTransferService} from "../services/data-transfer.service";

@Component({
  selector: "app-wiki",
  templateUrl: "./wiki.page.html",
  styleUrls: ["./wiki.page.scss"],
})
export class WikiPage implements OnInit {
  public docName: String;
  public wikiPage!: ParsedQueryResponseDocument;
  public paragraph_id: string;
  private router: Router;
  private data = inject(DataService);
  private dataTransferService = inject(DataTransferService);
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

    let paragraph = this.dataTransferService.getData().text[0]

    Object.keys(this.wikiPage.text).forEach((text: string, index) => {
      if (text === paragraph){
        this.paragraph_id = '#' + index;
      }
    });

    this.addParagraphIdentifierToRoute()

  }

  addParagraphIdentifierToRoute() {
    this.router.navigate([], {
      relativeTo: this.activatedRoute,
      fragment: this.paragraph_id,
      queryParamsHandling: 'preserve'
    });
  }

  getBackButtonText() {
    const isIos = this.platform.is('ios')
    return isIos ? 'Inbox' : '';
  }

  protected readonly ParsedDocumentTextTypes = ParsedDocumentTextTypes;
}
