import {
  AfterViewChecked,
  AfterViewInit,
  ChangeDetectorRef,
  Component,
  ElementRef,
  inject,
  OnInit,
  ViewChild
} from "@angular/core";

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
export class WikiPage implements OnInit, AfterViewChecked, AfterViewInit {
  public docName: String;
  public wikiPage!: ParsedQueryResponseDocument;
  public paragraph_id: string;
  private data = inject(DataService);
  private dataTransferService = inject(DataTransferService);
  private activatedRoute = inject(ActivatedRoute);
  private platform = inject(Platform);
  private scrolledToParagraph: boolean = false;
  private paragraphFound: boolean = false;

  @ViewChild('searchBar')
  searchBar: IonSearchbar;

  searchText: string = '';

  constructor(private router: Router, private route: ActivatedRoute, private cdRef: ChangeDetectorRef, private el: ElementRef) {
  }

  ngOnInit() {
    this.docName = this.activatedRoute.snapshot.paramMap.get('id') as string;
    const idx = this.activatedRoute.snapshot.paramMap.get('id') as string;
    this.data.getDocomentById(parseInt(idx, 10)).then((res) => {
      this.wikiPage = ResponseParsingService.parseDocumentResponse(res);
      this.scrolledToParagraph = false
    });
    this.route.queryParams.subscribe((p) => {
      this.searchText = p['query'];
    });
  }

  ngAfterViewInit() {
  }

  ngAfterViewChecked() {
    this.cdRef.detectChanges();

    if (!this.paragraphFound) {
      this.checkParagraphs();
    }

    if (this.paragraph_id && !this.scrolledToParagraph) {
      this.scrollToParagraph();
      this.scrolledToParagraph = true;
    }

  }

  private checkParagraphs(){
      let search_result = this.removeBracketedText(this.dataTransferService.getData().passage)
      search_result = this.transform(search_result)

      const pageParagraphs = this.el.nativeElement.querySelectorAll('p');
      pageParagraphs.forEach((pageParagraph: HTMLElement) => {
        if (pageParagraph.innerText.trim().includes(search_result)) {
          this.paragraph_id = pageParagraph.id;
          this.paragraphFound = true;
        }
        else if (search_result.includes(pageParagraph.innerText.trim())) {
          this.paragraph_id = pageParagraph.id;
          this.paragraphFound = true;
        }
      });
  }

  private scrollToParagraph() {
    setTimeout(() => {
      const paragraphElement = document.getElementById(this.paragraph_id);
      if (paragraphElement) {
        paragraphElement.scrollIntoView({behavior: 'smooth', block: 'center'});
      }
    }, 0);
  }

  private transform(value: string): string {
    if (!value) return '';
    let result = value.replace(/<\/?[^>]+(>|$)/g, '');
    const textArea = document.createElement('textarea');
    textArea.innerHTML = result;
    result = textArea.value;

    const index= result.indexOf('[');
    if (index !== -1) {
      const substring = result.substring(index);
      if (substring.startsWith('[https')) {
        result = result.substring(0, index).trim();
      }
    }

    return result;
  }

  private removeBracketedText(input: string): string {
    return input.replace(/\[.*?]/, "").trim();
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
      queryParams: {query: this.searchText},
    });
  }

  protected readonly ParsedDocumentTextTypes = ParsedDocumentTextTypes;
}
