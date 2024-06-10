import { Component, inject, OnInit, ViewChild } from '@angular/core';

import { DataService } from '../services/data.service';
import { IonSearchbar, Platform } from '@ionic/angular';
import {
  ParsedDocumentTextTypes,
  ParsedQueryResponseDocument,
} from '../types/query-response.type';
import { ActivatedRoute, Router } from '@angular/router';
import { ResponseParsingService } from '../services/response-parsing-service';

@Component({
  selector: 'app-wiki',
  templateUrl: './wiki.page.html',
  styleUrls: ['./wiki.page.scss'],
})
export class WikiPage implements OnInit {
  public docName: String;
  public wikiPage!: ParsedQueryResponseDocument;
  public createdHeaders: string[] = [];
  private data = inject(DataService);
  private activatedRoute = inject(ActivatedRoute);
  private platform = inject(Platform);

  @ViewChild('searchBar')
  searchBar: IonSearchbar;

  searchText: string = '';

  constructor(private router: Router, private route: ActivatedRoute) {}

  ngOnInit() {
    this.docName = this.activatedRoute.snapshot.paramMap.get('id') as string;
    const idx = this.activatedRoute.snapshot.paramMap.get('id') as string;
    this.data.getDocomentById(parseInt(idx, 10)).then((res) => {
      this.wikiPage = ResponseParsingService.parseDocumentResponse(res);
    });
    this.route.queryParams.subscribe((p) => {
      this.searchText = p['query'];
    });
  }

  getBackButtonText() {
    const isIos = this.platform.is('ios');
    return isIos ? 'Inbox' : '';
  }

  addCreatedHeader(header: string) {
    this.createdHeaders.push(header);
  }

  isHeaderAlreadyCreated(header: string): boolean {
    return this.createdHeaders.includes(header);
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
