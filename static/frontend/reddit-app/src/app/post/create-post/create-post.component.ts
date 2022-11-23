import { Component, OnInit, AfterViewInit, NgZone, ViewChild, ElementRef, ChangeDetectorRef } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { DatePipe } from '@angular/common';

import { debounceTime, distinctUntilChanged } from "rxjs/operators";
import { MatDialog } from '@angular/material/dialog';
import { HttpEventType } from '@angular/common/http';
import FroalaEditor from 'froala-editor';
import { PostService } from '@reddit/core/services/post/post.service';
import { UserService } from '@reddit/core/services/user/user.service';
import { User } from '@reddit/core/models/user.model';


@Component({
  selector: 'app-create-post',
  templateUrl: './create-post.component.html',
  styleUrls: ['./create-post.component.scss']
})
export class CreatePostComponent implements OnInit {
  public editor;

  blogForm: FormGroup;
  content: any;
  user: User;
  isLoading: boolean = true;
  userGroups: [] = [];
  selected: null;
  formData: any;

  constructor(
    private postService: PostService,
    private userService: UserService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.initializeForm();
    this.getAuthUser();
    this.isLoading = false;
  }

  initializeForm() {
    this.blogForm = new FormGroup({
      title: new FormControl('', {
        validators: [Validators.required]
      }),
      content: new FormControl(this.content, {
        validators: [Validators.required]
      })
    });

    this.blogForm.valueChanges
      .pipe(debounceTime(3000), distinctUntilChanged())
      .subscribe(
        (response) => {
          console.log(response);
        });
  }

  public options: Object = {
    iframe: true,
    attribution: false,
    autofocus: true,
    placeholderText: 'Add content',
    fontFamilyDefaultSelection: 'Roboto',
    charCounterCount: true,
    toolbarInline: false,
    spellcheck: true,
    tooltips: false,
    multiLine: true,
    pastePlain: true,
    heightMin: 400,
    quickInsertEnabled: false,
    pluginsEnabled: ['aviary', 'image', 'fontFamily', 'fontSize', 'help', 'colors', 'paragraphStyle', 'align', 'lists', 'outdent', 'indent', 'paragraphFormat', 'specialCharacters', 'hr', 'clearFormatting', 'link', 'embedly', 'file', 'table', 'undo', 'redo', 'spellchecker'],
    toolbarButtons: {
      'moreText': {
        'buttons': ['bold', 'italic', 'underline', 'strikeThrough', 'subscript', 'superscript'],
        'buttonsVisible': 6
      },
      'moreParagraph': {
        'buttons': ['alignLeft', 'alignCenter', 'formatOLSimple', 'alignRight', 'alignJustify', 'formatOL', 'formatUL', 'quote'],
        'buttonsVisible': 5
      },
      'moreRich': {
        'buttons': ['insertLink', 'insertImage', 'insertVideo', 'insertTable', 'insertFile'],
        align: 'left',
        'buttonsVisible': 3
      },
      'moreMisc': {
        'buttons': ['undo', 'redo', 'help'],
        align: 'left',
        'buttonsVisible': 3
      }
    },
    imageAddNewLine: true,
    imageDefaultMargin: 7,
    imageEditButtons: ['imageReplace', 'imageAlign', 'imageCaption', 'imageRemove', 'imageDisplay',
      'imageSize', 'imageStyle', 'imageAlt'],
    imageInsertButtons: ['imageBack', '|', 'imageUpload', 'imageByURL', 'imageManager'],
    imageMove: false,
    imagePaste: false,
    imageResizeWithPercent: true, // sets image size in percent
    imageDefaultWidth: 100, // sets default as 100%
    videoResponsive: true,
    videoInsertButtons: ['videoBack', '|', 'videoEmbed', 'videoByURL',],
    videoAllowedTypes: ['mp4'],
    videoAllowedProviders: ['youtube', 'vimeo'],
    videoEditButtons: ['videoReplace', 'videoRemove'],
    videoUpload: false,
    videoResize: false,
    videoSplitHTML: true,
    linkInsertButtons: ['linkBack'],
    events: {
      'initialized': function(e, that = this) {
        console.log(e);
      },
      'video.inserted': () => {
      },
      'video.removed': () => {
      },
      'image.uploaded': () => {
      },
      'image.removed': () => {
      },
    }
  }

  public initializeFroala(initControls) {
    initControls.initialize();
    this.editor = initControls.getEditor();
  }

  getAuthUser(): void {
    this.userService.userInitialized.subscribe(
      (initialized: boolean) => {
        if (initialized) {
          this.userService.user.subscribe(
            (user: User) => {
              this.user = user;
            });
        }
      });
  }

  submit() {
    const data = {
      title: this.blogForm.controls.title.value,
      content: this.blogForm.controls.content.value,
      author: this.user.id
    }

    this.postService.createPost(data).subscribe(
      (response: any) => {
        this.router.navigate(['', response.uuid])
      }
    )
  }

  // onFileSelected(files: any) {
  //   const file:File = files[0];
  //   if(file) {
  //     this.formData = new FormData();
  //     this.formData.append("image", file);
  //   }
  // }

}
