import {
  ChangeDetectionStrategy,
  Component,
  inject,
  Input,
} from '@angular/core';
import { Platform } from '@ionic/angular';
import {QueryResponseResult} from "../types/query-response.type";
import {DataTransferService} from "../services/data-transfer.service";

@Component({
  selector: 'app-search-answer',
  templateUrl: './search-answer.component.html',
  styleUrls: ['./search-answer.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SearchAnswerComponent {
  private platform = inject(Platform);
  private dataTransferService = inject(DataTransferService);
  @Input() queryResponseResult: QueryResponseResult;
  @Input() query: String;
  isIos() {
    return this.platform.is('ios');
  }

  sendData(): void {
    this.dataTransferService.setData(this.queryResponseResult)
  }
}
