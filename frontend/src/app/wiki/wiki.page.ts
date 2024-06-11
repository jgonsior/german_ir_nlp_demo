import {AfterViewChecked, Component, inject, OnInit, ViewChild} from "@angular/core";

import {DataService} from "../services/data.service";
import {IonSearchbar, Platform} from "@ionic/angular";
import {ParsedDocumentTextTypes, ParsedQueryResponseDocument,} from "../types/query-response.type";
import {ActivatedRoute, Router} from "@angular/router";
import {ResponseParsingService} from "../services/response-parsing-service";
import {DataTransferService} from "../services/data-transfer.service";

@Component({
  selector: 'app-wiki',
  templateUrl: './wiki.page.html',
  styleUrls: ['./wiki.page.scss'],
})
export class WikiPage implements OnInit, AfterViewChecked {
  public docName: String;
  public wikiPage!: ParsedQueryResponseDocument;
  public paragraph_id!: string;
  private data = inject(DataService);
  private dataTransferService = inject(DataTransferService);
  private activatedRoute = inject(ActivatedRoute);
  private platform = inject(Platform);

  @ViewChild('searchBar')
  searchBar: IonSearchbar;

  searchText: string = '';

  constructor(private router: Router, private route: ActivatedRoute) {
  }

  ngOnInit() {
    this.docName = this.activatedRoute.snapshot.paramMap.get('id') as string;
    const idx = this.activatedRoute.snapshot.paramMap.get('id') as string;
    this.data.getDocomentById(parseInt(idx, 10)).then((res) => {
      this.wikiPage = ResponseParsingService.parseDocumentResponse(res);
      console.log('wikiData', this.wikiPage);

      let search_result = this.dataTransferService.getData()
      console.log('Query Response Data', search_result)

      let paragraphs = this.wikiPage.text.
      filter((item) => item.type == ParsedDocumentTextTypes.normal_text_passage)
        .map((item) => {
        return item.content;
      });

      paragraphs.forEach((text, index) => {
        if (search_result.passage.includes(text)) {
          console.log('Check yielded true');
          this.paragraph_id = '#' + index;
          console.log(this.paragraph_id);
        }
      });
    });
    this.route.queryParams.subscribe((p) => {
      this.searchText = p['query'];
    });
  }

  ngAfterViewChecked() {
    this.scrollToParagraph();
  }

  scrollToParagraph() {
    setTimeout(() => {
      const paragraphElement = document.getElementById(this.paragraph_id);
      console.log('paragraphElement', paragraphElement);
      if (paragraphElement) {
        paragraphElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 0);
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
