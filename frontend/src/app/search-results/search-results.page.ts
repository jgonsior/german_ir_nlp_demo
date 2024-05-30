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

@Component({
  selector: 'app-search-results',
  templateUrl: './search-results.page.html',
  styleUrls: ['./search-results.page.scss'],
})
export class SearchResultsPage implements OnInit {
  private data = inject(DataService);
  protected queryResults: QueryResponseResult[] = [];
  private platform = inject(Platform);

  @ViewChild('searchBar')
  searchBar: IonSearchbar;

  searchText: string = '';

  constructor(private route: ActivatedRoute, private router: Router) {
    this.getMessages();
  }
  ngOnInit(): void {
    var q = this.route.snapshot.queryParamMap.get('query');

    if (q != null) {
      this.searchText = q;
      this.data.changeSearchText(this.searchText);
    }
      
  }

  refresh(event: any) {
    this.getMessages();
    setTimeout(() => {
      (event as RefresherCustomEvent).detail.complete();
    }, 3000);
  }

  async getMessages() {
    var q = this.route.snapshot.queryParamMap.get('query');

    if (q == null) return;

    await this.data.getQueryResults(q).then((response) => {
      // this.queryResults = Array(this.count).fill(response[0]);
      this.queryResults = response;
    });
  }

  async onIonInfinite(ev: any) {
    var q = this.route.snapshot.queryParamMap.get('query');

    if (q == null) return;

    await this.data.getQueryResults(q).then((response) => {
      this.queryResults.push(...response);
    });
    setTimeout(() => {
      (ev as InfiniteScrollCustomEvent).target.complete();
    }, 500);
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
