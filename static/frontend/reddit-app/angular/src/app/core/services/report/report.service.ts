import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '@reddit/env/environment';

@Injectable({
  providedIn: 'root'
})
export class ReportService {
  private baseUrl = `${environment.serverUrl}${environment.baseUrl}`;

  constructor(private http: HttpClient) {
  }

  getReportTypes() {
    return this.http.get(this.baseUrl + 'report_types/');
  }

  createReport(post_uuid: string, report) {
    return this.http.post(this.baseUrl + 'posts/' + post_uuid + '/reports/', report);
  }

  redactReport(post_uuid: string, report_id: number) {
    return this.http.put(this.baseUrl + 'posts/' + post_uuid + '/reports/' + report_id + '/redact/', {});
  }
}
