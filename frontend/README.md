# Frontend

This folder of the repository `german_ir_nlp_demo` contains the code and resources used during the Long Night of Science and 
Technology (LNDW). It includes various scripts, data sets, and other materials created for the event.

---
Prerequisites
---

### How to start

- Install node & npm
- Install ionic cli global: `npm install -g @ionic/cli`
- Run ionic project: `ionic serve`

### How to build the application for lndw

- Follow the setup instructions
- install the dependencies: `npm i`
- use the ionic serve option
- run `ionic serve --prod --no-livereload`
- use one of the following
- run `ionic build --prod`
- run `cd www && npx http-server` or serve by any other webserver

## Overall Structure

The Frontend for the `german_ir_nlp_demo` consists of three main pages. The pages include a `homepage`, a `search-result page` and
a `wikipage`. Additionally, there is an `error page` that intercepts any errors that may happen and visualizes that there was an
error. For better implementation the logic of the Frontend is divided into multiple components such that they can be worked on
separately. Furthermore, there are special predefined types that are required for the frontend to work properly.
For each of the components and for the types a folder exists in `./src/app`.

In the first section the `styling` of the Frontend is explained. The second section consists of the explanation of the `services`
and their functionality used in the Frontend. The third section includes an explanation of the logic of the `homepage` and
`search-result` page. The last section explains the main functionality of the `wikipage`.

### Environment Variables

All environment variables can be found in `./src/environments`. The main variables to note here are the `baseUrl` and 
`embeddingColor`. The `baseUrl` variable is used to specify the URL that the backend API is deployed to. The 
`embeddingColor` variable is used to specify the color for the background of the important words in the `wikipage`.

---

# 1. Styling

Each component has its own styling in the respective component folder, as an example [see](src\app\home\home.page.scss).
However, adjustments for the searchbars and the large viewport were made in [global.scss](src\global.scss).
The individual colours and other variables are also stored in [variables.scss](src\theme\variables.scss).
The main colours used in the application contain --ion-color-custom-\* in the name and are coordinated with the cover image,
which belongs to the home component.

## Used Images

All images used are AI generated. The image of the home component was generated with the Microsoft AI Image Generator,
[see](https://create.microsoft.com/en-us/features/ai-image-generator), and then customised according to the requirements.
The other images were generated with the Ai Generator from deepai [see](https://deepai.org/machine-learning-model/text2img)

An image with the corresponding settings to maintain the same style can be found [here](src\theme\Image.PNG)
*Please note that it may be necessary to generate several times until the desired style is achieved.*

---

# 2. Services

In this section an explanation of the main services used in the frontend are explained. Therefore, it takes a look
the `DataService`, the `DataTransferService`, the `ResponseParsingService` and the `SimpleHTTPInterceptor`. All the
important files for the services can be found in `./src/app/services`.

## DataService and SimpleHTTPInterceptor

The httpclient gets injected per DI. The IP addresses of the backend server are defined in the `environment.ts` and 
`environment.prod.ts` files depending on the flavor. The classes are automatically parsed based on the specified 
classes. Errors are caught by the HttpInterceptor and forwarded to the error page.

```ts
  public async getQueryResults(query: String): Promise<QueryResponseResult[]> {
    const response = await lastValueFrom(this.httpClient.get<QueryResponseResult[]>(`${environment.baseUrl}/search?q=${query}`));

    return response;
  }

  public async getDocomentById(id: number) {
    return await lastValueFrom(this.httpClient.get<QueryResponseDocument>(`${environment.baseUrl}/document?id=${id}`));
  }

  public async getWordEmbedding(paragraph: String, query: String) {
    return await lastValueFrom(this.httpClient.post<WordEmbedding[]>(`${environment.baseUrl}/word_embeddings`, {'paragraph': paragraph, 'query': query}));
  }
```

```ts
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
          if(!req.url.includes('word_embeddings')) {
            this.router.navigateByUrl('/error')
          }
        }

        console.error(errorMessage ? errorMessage : returnedError);

        return of(returnedError);
      })
    )
}
```

## DataTransferService

The `DataTransferService` is a simple service to get and set data when transitioning from the `search-result` page to the 
`wikipage`. It consists of two simple methods which are `setData()` and `getData()`. This service is able to send data 
via the different components when a specific interaction on the `search-result` page is performed. It is needed to 
not pollute the url with unnecessary information. For the `wikipage` it is used to provide the original paragraph ranked 
in the ColBERT model to highlight and scroll to on the `wikipage` for the document. The most important part of the service
is show in the code snippet below:

```ts
setData(data: QueryResponseResult): void {
  this.data = data;
}

getData(): QueryResponseResult {
  return this.data;
}
```

## ResponseParsingService

This service is used to parse the text information of a retrieved document from the Backend API. The Service takes 
the text information stored in the `QueryResponseDocument` and filters the headings and paragraphs into their
respective order. This is done by splitting the text off the heading in [] brackets that is in front of every string
in the list of strings contain in the `QueryResponseDocument`. If the heading in front of the string has been seen 
already the following text is added to the headings paragraphs if the heading hasn't been seen it is added as a new
heading. If there are multiple headings following after each other in brackets a depth variable is increased for 
every heading to keep track of the headings position in the original document. In the following code snippet the 
most important parts of the `ResponseParsingService` are shown:

```ts
static parseDocumentResponse(response: QueryResponseDocument): ParsedQueryResponseDocument {
  const parsedDocument: ParsedQueryResponseDocument = {title: response.title, text: []};
  for (let textPassage of response.text) {
    let text = ''
    if(textPassage.startsWith('[') && textPassage.includes(']')){
      const headerSection = textPassage.split(']')[0].replace('[', '')
      const headers = headerSection.split(', ');
      let i = 0;
      for (let header of headers) {
        if(!this.wasHeadingCreated(parsedDocument, this.unescapeHtml(header))) {
          parsedDocument.text.push({
            type: ParsedDocumentTextTypes.heading,
            depth: i,
            content: this.unescapeHtml(header)
          });
          i++;
        }
      }
      text = textPassage.split(']')[1]
    }else{
      text = textPassage
    }
    parsedDocument.text.push({
      type: ParsedDocumentTextTypes.normal_text_passage,
      depth: 0,
      content: text
    });
  }
  return parsedDocument;
}
```

---

# 3. Home Page and Search Results Page

The homepage is based on the UI structure of other major search engines. The view is minimalist and is intended to guide the user in a targeted manner.

The search-results page uses paging for loading small chunks of data. Ionic's `ion-infinite-scroll` is used here. On every page that contains a 
searchbar (except for the homepage) a listener is registered on the query parameters of the URL in order to always adapt the input of the 
searchbar to the current query. To enable optimal UI handling for mobile versions, a swipe-to-refresh function has also been implemented.

The design of a single search result is implemented as a separate component `search-answer`. It is connected by code in the `search-results` list.

```angular17html
<app-search-answer
  *ngFor="let queryResponseResult of queryResults"
  [queryResponseResult]="queryResponseResult"
  [query]="searchText"
>
</app-search-answer>
```

New Components can be automatically generated by `ionic generate page [name]` or `ionic generate component [name]`

Angular's two-way binding is the easiest way to connect an input field with the component class. Simply add an `[(ngModel)]="searchText"` to the 
input and the corresponding string variable to the component class.

---

# 4. WikiPage

All code and files need for this component to work can be found in `./src/app/wiki`. The most important files for the functionality of
the wiki page are `wiki.page.ts` and `wiki.page.html`.

## Functionality

`wiki.page.ts`
`wiki.page.html`

These two source files handle all wiki page related logic. They incorporate data preparation for the view creation, scroll logic to put the
retrieved paragraph from ColBERT into view and creation of the background for the important words that lead to ColBert identifying
the paragraph as an answer to the query.

## View Creation

To accomplish the data preparation for the view creation the data for the current document is first retrieved from the backend API
via the data service found in `./src/app/services`. The method called from the `DataService` is `getDocumentById(docID)` which is
given the currently clicked DocID from the interaction with the `seach-results` page. The next step is to transform the document
data received into an iterable data structure with seperated heading identifiers and their associated paragraphs. This is done by
the response parsing service which is called with data retrieved for the document through the function `parseDocumentResponse`.
The parsed data is then used to create the page in `wiki.page.html`. The first important step is to check the availability of the
data this is done through the `*ngIf` statement. When the data is available a `*ngFor` loop creates the paragraphs and headings
depending on the current type of the string read from the list of text contained in `wikiPage.text`. If it is a heading the depth
associated with the heading through `passages.depth` defines the heading type. The higher the depth number the lower the heading.
If the type check yields `normal_text_passage` the text is put into a paragraph with an ID and shown under the current heading.
The code snipped shown now is the full code used to build the view:

```angular17html
<ion-col size="6" class="ion-padding wiki__column" *ngIf="wikiPage">
  <ng-container *ngFor="let passages of wikiPage.text; let i = index">
    <ng-container
      *ngIf="passages.type === ParsedDocumentTextTypes.heading"
    >
      <h2 *ngIf="passages.depth === 0">{{ passages.content }}</h2>
      <h3 *ngIf="passages.depth === 1">{{ passages.content }}</h3>
      <h4 *ngIf="passages.depth === 2">{{ passages.content }}</h4>
      <h5 *ngIf="passages.depth === 3">{{ passages.content }}</h5>
    </ng-container>
    <ng-container *ngIf="passages.type === ParsedDocumentTextTypes.normal_text_passage">
      <p id="#{{i}}" *ngIf="compareParagraphs(searchedParagraph, passages.content); else noEmbeddings">
        <ng-container  *ngFor="let word of wordembeddings">
          <span [ngStyle]="{'background-color': createColorFromEmbedding(word)}">{{word.word}} </span>
        </ng-container>
      </p>
      <ng-template #noEmbeddings><p id="#{{i}}">{{passages.content}}</p></ng-template>
    </ng-container>
  </ng-container>
</ion-col>
```

## Scroll Logic

To accomplish the scroll logic to put the by ColBERT as answer evaluated paragraph of the document into view the wiki page needs the paragraph
associated with the document from the original response for the `search-results`. To receive the original data there is a
`DataTransferService` which can be found in `./src/app/services` under `data-transfer.service.ts`. This `DataTransferService` provides
an interface to transfer data between the `search-result` and the `WikiPage` via the simple methods `setData(Data)` and `getData()`.
With the data from the original search results available we can now compare the text of the important paragraph with all text in
paragraphs contained in the `WikiPage` and find the ID of the paragraph that the scroll logic is supposed to put into view. When the ID of the
paragraph is found the actual scrolling method `scrollToParagraph()` is called. The most important code snippets can be viewed in the
following:

```typescript

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

private checkParagraphs() {
  let search_result = this.removeBracketedText(this.dataTransferService.getData().passage)
  search_result = this.transform(search_result)

  const pageParagraphs = this.el.nativeElement.querySelectorAll('p');
  pageParagraphs.forEach((pageParagraph: HTMLElement) => {
    if (pageParagraph.innerText.trim().includes(search_result)) {
      this.paragraph_id = pageParagraph.id;
      this.paragraphFound = true;
    } else if (search_result.includes(pageParagraph.innerText.trim())) {
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
```

## Word Embeddings

To accomplish the coloring for the embeddings the paragraph associated with the currently shown document is needed again. Since the data is also needed
for the scroll logic it can be reused in this logic. The comparison is done during the view creation process as the coloring information for the embeddings
is a background behind the word for which an embedding is found. For that purpose a comparison between the currently created paragraph
and the important paragraphs text content is done as in the view creation in `wiki.page.html`. If the correct paragraph is found the backgrounds are created
by the function `createColorFromEmbedding()` using the embedding values. The embedding values are retrieved by using the provided API from the backend
through the `DataService` and the method `getWordEmbedding()`. These embedding values are then used to set the alpha value of the color used for the
background. The color used for the background can be set in either environment variable file `environment.ts` or `environment.prod.ts`.
In the following the most important snippets from both the `wiki.page.html` and `wiki.page.ts` are shown:

```angular17html

<ng-container *ngIf="passages.type === ParsedDocumentTextTypes.normal_text_passage">
    <p id="#{{i}}" *ngIf="compareParagraphs(searchedParagraph, passages.content); else noEmbeddings">
      <ng-container  *ngFor="let word of wordembeddings">
        <span [ngStyle]="{'background-color': createColorFromEmbedding(word)}">{{word.word}} </span>
      </ng-container>
    </p>
    <ng-template #noEmbeddings><p id="#{{i}}">{{passages.content}}</p></ng-template>
</ng-container>
```

```typescript

ngOnInit() {
  this.data.getDocomentById(parseInt(idx, 10)).then((res) => {
    let search_result = this.dataTransferService.getData()
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
    });
}

compareParagraphs(searchedParagraph: string, strcompare: string) {
  return searchedParagraph.replace(/\s/g, '').includes(strcompare.replace(/\s/g, '')) || strcompare.replace(/\s/g, '').includes(searchedParagraph.replace(/\s/g, ''));
}

createColorFromEmbedding(embedding: WordEmbedding) {
  return Color(environment.embeddingColor).alpha(embedding.embedding);
}

```
