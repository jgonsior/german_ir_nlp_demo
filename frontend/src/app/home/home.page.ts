import {
  Component,
  ElementRef,
  HostListener,
  ViewChild,
  inject,
} from '@angular/core';
import { IonButton, IonSearchbar, RefresherCustomEvent } from '@ionic/angular';
import { MessageComponent } from '../message/message.component';

import { DataService } from '../services/data.service';
import { QueryResponseResult } from '../types/query-response.type';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {
  @ViewChild('searchBar')
  searchBar: IonSearchbar;

  @ViewChild('searchButton')
  searchButton: IonButton;

  @HostListener('window:resize', ['$event.target.innerWidth'])
  handleWindowResize(innerWidth: number) {
    this.searchButton.size = innerWidth >= 600 ? 'large' : 'default';
  }

  getWindowWidth(): number {
    return window.innerWidth;
  }

  searchText: string = '';

  constructor(private router: Router) {}

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
}