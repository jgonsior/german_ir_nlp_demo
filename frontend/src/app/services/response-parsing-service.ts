import {
  ParsedDocumentTextTypes,
  ParsedQueryResponseDocument,
  QueryResponseDocument
} from "../types/query-response.type";

export class ResponseParsingService {

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

  static wasHeadingCreated(parsedDocument: ParsedQueryResponseDocument, heading: string): boolean {
    if (parsedDocument.text.length == 0) {
      return false;
    }
    const foundHeading = parsedDocument.text.find((value) => {
      return value.type === ParsedDocumentTextTypes.heading && value.content == heading;
    })
    return foundHeading !== undefined
  }

  static unescapeHtml(safe: string) {
    return safe
      // For security reasons we will not allow the construction of html tags
      // .replace(/&lt;/g, "<")
      .replace(/&amp;/g, "&")
      .replace(/&gt;/g, ">")
      .replace(/\"\=\= (\w+) \=/g, "$1");
  }
}
