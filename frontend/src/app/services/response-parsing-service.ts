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
          if(!this.wasHeadingCreated(parsedDocument, header)) {
            parsedDocument.text.push({
              type: ParsedDocumentTextTypes.heading,
              depth: i,
              content: header
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
}