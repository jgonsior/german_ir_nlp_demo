import {AfterViewChecked, ChangeDetectorRef, Component, inject, OnInit, ViewChild} from "@angular/core";

import {DataService} from "../services/data.service";
import {IonSearchbar, Platform} from "@ionic/angular";
import {ParsedDocumentTextTypes, ParsedQueryResponseDocument,} from "../types/query-response.type";
import {ActivatedRoute, Router} from "@angular/router";
import {ResponseParsingService} from "../services/response-parsing-service";
import {DataTransferService} from "../services/data-transfer.service";
import {search} from "ionicons/icons";

@Component({
  selector: 'app-wiki',
  templateUrl: './wiki.page.html',
  styleUrls: ['./wiki.page.scss'],
})
export class WikiPage implements OnInit, AfterViewChecked {
  public docName: String;
  public wikiPage!: ParsedQueryResponseDocument;
  public paragraph_id: string;
  private data = inject(DataService);
  private dataTransferService = inject(DataTransferService);
  private activatedRoute = inject(ActivatedRoute);
  private platform = inject(Platform);
  private scrolledToParagraph: boolean = false;

  @ViewChild('searchBar')
  searchBar: IonSearchbar;

  searchText: string = '';

  constructor(private router: Router, private route: ActivatedRoute, private cdRef: ChangeDetectorRef) {
  }

  ngOnInit() {
    this.docName = this.activatedRoute.snapshot.paramMap.get('id') as string;
    const idx = this.activatedRoute.snapshot.paramMap.get('id') as string;
    this.data.getDocomentById(parseInt(idx, 10)).then((res) => {
      this.wikiPage = ResponseParsingService.parseDocumentResponse(res);
      this.scrolledToParagraph = false

      let search_result = this.removeBracketedText(this.dataTransferService.getData().passage)
      let paragraphs = this.wikiPage.text.
      filter((item) => item.type == ParsedDocumentTextTypes.normal_text_passage)
        .map((item) => {
        return item.content;
      });

      let paragraph_found = false;
      paragraphs.forEach((text, index) => {
        if (!paragraph_found) {
          if (search_result.includes(text)) {
            this.paragraph_id = this.getParagraphIdByContent(text);
            paragraph_found = true;
          }
          else if (text.includes(search_result)) {
            this.paragraph_id = this.getParagraphIdByContent(text);
            paragraph_found = true;
          }
        }
      });
    });
    this.route.queryParams.subscribe((p) => {
      this.searchText = p['query'];
    });
  }

  ngAfterViewChecked() {
    this.cdRef.detectChanges();
    console.log(this.paragraph_id, this.scrolledToParagraph);
    if (this.paragraph_id && !this.scrolledToParagraph) {
      this.scrollToParagraph();
      this.scrolledToParagraph = true;
    }

  }

  private scrollToParagraph() {
    setTimeout(() => {
      const paragraphElement = document.getElementById(this.paragraph_id);
      console.log('paragraphElement', paragraphElement);
      if (paragraphElement) {
        paragraphElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 0);
  }

  private removeBracketedText(input: string): string {
    return input.replace(/\[.*?]/, "").trim();
  }

  private getParagraphIdByContent(content: string): string {
    let lst_para = document.getElementsByTagName('p');
    console.log(lst_para)
    for (let ind = 0; ind < lst_para.length; ind++) {
      const pt = lst_para[ind];
      console.log(content)
      console.log(pt);
      if (pt.innerText === content) {
        return pt.id;
      }
    }

    return "#"
  }

  getBackButtonText() {
    const isIos = this.platform.is('ios')
    return isIos ? 'Inbox' : '';
  }

  onSearchClicked() {
    if (this.searchText.trim().length == 0) {
      this.searchBar.getInputElement().then((inputElement) => {
        this.searchText = '';
        inputElement.blur();
      });
      return;
    }

    this.router.navigate(['/search-results'], {
      queryParams: { query: this.searchText },
    });
  }

  protected readonly ParsedDocumentTextTypes = ParsedDocumentTextTypes;
}
