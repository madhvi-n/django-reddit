import { Component, Inject, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { FormControl, Validators } from '@angular/forms';
import { ReportService } from '@reddit/core/services/report/report.service';

@Component({
  selector: 'app-report-dialog',
  templateUrl: './report-dialog.component.html',
  styleUrls: ['./report-dialog.component.scss']
})
export class ReportDialogComponent implements OnInit {
  public validateUrlRegex = /(^|\s)((https?:\/\/)?[\w-]+(\.[\w-]+)+\.?(:\d+)?(\/\S*)?)/gi;
  reportInfoControl: FormControl = new FormControl();
  urlControl: FormControl = new FormControl('', {
    validators: [Validators.required, Validators.pattern(this.validateUrlRegex)]
  });
  typeControl: FormControl = new FormControl();
  reporter: number;
  reported_user: string;
  selectedType: number;
  readOnlyUrl: boolean;
  types = [];

  constructor(
    public dialogRef: MatDialogRef<ReportDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private reportService: ReportService
  ) { }

  ngOnInit(): void {
    // this.isLoading = true;
    // this.slug = this.data.slug ? this.data.slug : null;
    // this.source = this.data.source;
    // if (!this.source || !this.sources.includes(this.source)) {
    //   throw new Error('A valid source is required');
    // }
    // this.reporter = this.data.user?.id;
    this.getReportTypes();
    // if (this.data.url) {
    //   this.urlControl.setValue(this.data.url);
    // } else {
    //   this.urlControl.setValue(window.location.href);
    // }
    // this.readOnlyUrl = this.urlControl.value ? true : false ;
  }

  getReportTypes(){
    this.reportService.getReportTypes().subscribe(
      (response: any) => {
        this.types = response;
      })
  }

  radioSelectEvent(event) {
    console.log(event);
    this.selectedType = event.value;
  }

  create() {
    this.dialogRef.close(this.selectedType);
  }

  closeDialog() {
    this.dialogRef.close();
  }
}
