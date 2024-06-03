import {Component, inject, OnInit} from "@angular/core";

import {DataService} from "../services/data.service";
import {Platform} from "@ionic/angular";
import {
  ParsedDocumentTextTypes,
  ParsedQueryResponseDocument,
} from "../types/query-response.type";
import {ActivatedRoute} from "@angular/router";
import {ResponseParsingService} from "../services/response-parsing-service";
import {WordEmbeddingResponse} from "../types/word-embedding-response";

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
  protected wordembeddings: WordEmbeddingResponse;
  protected searchedParagraph: string;

  constructor() {
  }

  ngOnInit() {
    this.docName = this.activatedRoute.snapshot.paramMap.get('id') as string;
    this.searchedParagraph = this.activatedRoute.snapshot.paramMap.get('paragraph') as string;
    const idx = this.activatedRoute.snapshot.paramMap.get('id') as string;
    this.data.getDocomentById(parseInt(idx, 10)).then((res) => {
      this.wikiPage = ResponseParsingService.parseDocumentResponse(res);
      console.log(this.wikiPage)
      this.data.getWordEmbedding(this.searchedParagraph).then((res) => {
        this.wordembeddings = res;
      })
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
