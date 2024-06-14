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
import {WordEmbedding} from "../types/word-embedding-response";
import Color from "color";

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
  protected wordembeddings: WordEmbedding[];
  protected searchedParagraph: string;

  @ViewChild('searchBar')
  searchBar: IonSearchbar;

  searchText: string = '';

  constructor(private router: Router, private route: ActivatedRoute, private cdRef: ChangeDetectorRef, private el: ElementRef) {
  }

  ngOnInit() {
    this.docName = this.activatedRoute.snapshot.paramMap.get('id') as string;
    const idx = this.activatedRoute.snapshot.paramMap.get('id') as string;
    const query = this.activatedRoute.snapshot.paramMap.get('query') as string;
    console.log(query)
    this.data.getDocomentById(parseInt(idx, 10)).then((res) => {
      this.wikiPage = ResponseParsingService.parseDocumentResponse(res);
      this.scrolledToParagraph = false
      console.log('wikiData', this.wikiPage);

      let search_result = this.dataTransferService.getData()
      this.searchedParagraph = ResponseParsingService.unescapeHtml(search_result.passage);
      console.log('Query Response Data', this.searchedParagraph);
      this.data.getWordEmbedding(search_result.passage, query).then((res) => {
        let shouldTrashHeading = false
        this.wordembeddings = res.filter((item) => {
          if (item.word.startsWith('[')) {
            shouldTrashHeading = true;
            return false;
          }
          if(shouldTrashHeading || item.word.endsWith(']')) {
            shouldTrashHeading = false
            return false;
          }
          return true;
        });
      })

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

  createColorFromEmbedding(embedding: WordEmbedding) {
    return Color('#0054ff').alpha(embedding.embedding);
  }

  compareParagraphs(searchedParagraph: string, strcompare: string) {
    return searchedParagraph.replace(/\s/g, '').includes(strcompare.replace(/\s/g, '')) || strcompare.replace(/\s/g, '').includes(searchedParagraph.replace(/\s/g, ''));
  }
}
