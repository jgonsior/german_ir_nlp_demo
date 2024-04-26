import { Component, OnInit, inject } from '@angular/core';
import { QueryResponseResult } from '../types/query-response.type';
import { RefresherCustomEvent } from '@ionic/angular';
import { DataService } from '../services/data.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-search-results',
  templateUrl: './search-results.page.html',
  styleUrls: ['./search-results.page.scss'],
})
export class SearchResultsPage implements OnInit  {
  private data = inject(DataService);
  protected queryResults: QueryResponseResult[] = [];


  constructor(private route: ActivatedRoute) { 
    this.getMessages();
  }
  ngOnInit(): void {
  }

  refresh(event: any) {
    setTimeout(() => {

      (event as RefresherCustomEvent).detail.complete();
    },3000);
  }

  async getMessages() {

    var q = this.route.snapshot.queryParamMap.get("query");

    if(q == null) return;

    await this.data.getQueryResults(q).then((response) => {
      this.queryResults = response;
    });
  }
}
