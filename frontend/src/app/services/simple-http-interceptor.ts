import {Injectable, Provider} from "@angular/core";
import {
  HTTP_INTERCEPTORS, HttpErrorResponse,
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest
} from "@angular/common/http";
import {catchError, Observable, of, retry} from "rxjs";
import {Router} from "@angular/router";

@Injectable()
export class SimpleHttpInterceptor implements HttpInterceptor {
  constructor(public router: Router) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(req)
      .pipe(
        retry(1),
        catchError((returnedError) => {
          let errorMessage = null;

          if (returnedError.error instanceof ErrorEvent) {
            errorMessage = `Error: ${returnedError.error.message}`;
          } else if (returnedError instanceof HttpErrorResponse) {
            errorMessage = `Error Status ${returnedError.status}: ${returnedError.error.error} - ${returnedError.error.message}`;
            this.router.navigateByUrl('/error')
          }

          console.error(errorMessage ? errorMessage : returnedError);

          return of(returnedError);
        })
      )
  }
}

export const simpleHttpInterceptorProvider: Provider =
  {provide: HTTP_INTERCEPTORS, useClass: SimpleHttpInterceptor, multi: true};
