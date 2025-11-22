import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
@Pipe({
  name: 'safeContent'
})
export class SafeContentPipe implements PipeTransform {
  constructor(private sanitizer:DomSanitizer){}
  transform(content: string) {
    return this.sanitizer.bypassSecurityTrustHtml(content);
    // return this.sanitizer.bypassSecurityTrustStyle(html);
    // return this.sanitizer.bypassSecurityTrustScript(html);
    // return this.sanitizer.bypassSecurityTrustUrl(html);
    // return this.sanitizer.bypassSecurityTrustResourceUrl(html);
  }
}
