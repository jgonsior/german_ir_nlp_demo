import {
  ChangeDetectionStrategy,
  Component,
  inject,
  Input,
} from '@angular/core';
import { Platform } from '@ionic/angular';
import { QueryResponseResult } from '../types/query-response.type';

@Component({
  selector: 'app-search-answer',
  templateUrl: './search-answer.component.html',
  styleUrls: ['./search-answer.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SearchAnswerComponent {
  private platform = inject(Platform);
  @Input() queryResponseResult?: QueryResponseResult;
  @Input() query: String;
  isIos() {
    return this.platform.is('ios');
  }
}
