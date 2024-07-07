## How to start

* Install node & npm
* Install ionic cli global: `npm install -g @ionic/cli`
* Run ionic project: `ionic serve`

## How to build the application for lndw

* Follow the setup instructions
* install the dependencies: `npm i`
* use the ionic serve option
* run `ionic serve --prod --no-livereload`
* use one of the following
* run `ionic build --prod`
* run `cd www && npx http-server` or serve by any other webserver

---

# 1. Styling

Each component has its own styling in the respective component folder, as an example [see](src\app\home\home.page.scss).
However, adjustments for the searchbars and the large viewport were made in [global.scss](src\global.scss).
The individual colours and other variables are also stored in [variables.scss](src\theme\variables.scss).
The main colours used in the application contain --ion-color-custom-* in the name and are coordinated with the cover image, 
which belongs to the home component.

## Verwendete Bilder

All images used are AI generated. The image of the home component was generated with the Microsoft AI Image Generator, 
[see](https://create.microsoft.com/en-us/features/ai-image-generator), and then customised according to the requirements.
The other images were generated with the Ai Generator from deepai [see](https://deepai.org/machine-learning-model/text2img)

An image with the corresponding settings to maintain the same style can be found [here](src\theme\Image.PNG)
*Please note that it may be necessary to generate several times until the desired style is achieved.

---
# 2. Services


---
# 3. Home Page and Search Results Page


---

# 2. WikiPage

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
With the data from the original search results available we can now compare the text of the  important paragraph with all text in 
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
