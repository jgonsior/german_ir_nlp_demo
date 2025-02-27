import { Component, OnInit, ViewChild, inject } from '@angular/core';
import { QueryResponseResult } from '../types/query-response.type';
import {
  InfiniteScrollCustomEvent,
  IonSearchbar,
  Platform,
  RefresherCustomEvent,
} from '@ionic/angular';
import { DataService } from '../services/data.service';
import { ActivatedRoute, Router } from '@angular/router';
import { LoadingController } from '@ionic/angular';

@Component({
  selector: 'app-search-results',
  templateUrl: './search-results.page.html',
  styleUrls: ['./search-results.page.scss'],
})
export class SearchResultsPage {
  private data = inject(DataService);
  protected queryResults: QueryResponseResult[] = [];
  private platform = inject(Platform);

  @ViewChild('searchBar')
  searchBar: IonSearchbar;

  searchText: string = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private loadingCtrl: LoadingController
  ) {
    route.queryParams.subscribe((p) => {
      if (this.searchText != p['query']) {
        this.searchText = p['query'];
        this.getMessages();
        this.queryResults = [];
      }
    });
  }

  refresh(event: any) {
    this.getMessages();
    (event as RefresherCustomEvent).detail.complete();
  }

  async getMessages() {
    const q = this.searchText;

    if (q == null) return;

    const loading = await this.loadingCtrl.create({
      message: 'Lade...',
      cssClass: 'custom-loading',
    });

    loading.present();

    await this.data.getQueryResults(q).then((response) => {
      this.queryResults = response;
      loading.dismiss();
    });
  }

  async onIonInfinite(ev: any) {
    const q = this.searchText;

    if (q == null) return;

    await this.data.getQueryResults(q).then((response) => {
      this.queryResults.push(...response);
    });
    (ev as InfiniteScrollCustomEvent).target.complete();
  }

  getBackButtonText() {
    const isIos = this.platform.is('ios');
    return isIos ? 'Inbox' : '';
  }

  navigateWithNewQuery() {
    if (this.searchText.trim().length == 0) {
      this.searchBar.getInputElement().then((inputElement) => {
        this.searchText = '';
        inputElement.blur();
      });
      return;
    }

    this.data.changeSearchText(this.searchText);
    this.router.navigate(['/search-results'], {
      queryParams: { query: this.searchText },
    });
    this.getMessages();
  }
}
