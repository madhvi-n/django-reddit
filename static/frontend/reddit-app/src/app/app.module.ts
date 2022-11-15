import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HTTP_INTERCEPTORS, HttpClientXsrfModule, HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { MaterialModule } from './material.module';
import { CookieService } from 'ngx-cookie-service';
import { AppComponent } from './app.component';
import { FeedComponent } from './feed/feed.component';
import { SignInComponent } from './auth/sign-in/sign-in.component';
import { SignUpComponent } from './auth/sign-up/sign-up.component';
import { SignOutComponent } from './auth/sign-out/sign-out.component';
import { AuthInterceptor } from './auth.interceptor';
import { HttpXsrfInterceptor } from './auth.header.interceptor';
import { PostComponent } from './components/post/post.component';
import { CreatePostComponent } from './components/create-post/create-post.component';
import { TimeSinceModule } from '@thisissoon/angular-timesince';
import { FroalaEditorModule, FroalaViewModule } from 'angular-froala-wysiwyg';
import { PostDetailComponent } from './components/post-detail/post-detail.component';
import { SearchComponent } from './components/search/search.component';
import { CommentGroupComponent } from './components/comment-group/comment-group.component';
import { CommentComponent } from './components/comment/comment.component';
import { CommentCreateComponent } from './components/comment-create/comment-create.component';
import { CommentEditComponent } from './components/comment-edit/comment-edit.component';
import { CommentFooterComponent } from './components/comment-footer/comment-footer.component';
// import { CommentUserComponent } from './components/comment-user/comment-user.component';
import { CommentListComponent } from './components/comment-list/comment-list.component';
import { ConfirmationDialogComponent } from './components/confirmation-dialog/confirmation-dialog.component';
import { FlexLayoutModule } from '@angular/flex-layout';
import { SafeContentPipe } from '@reddit/core/pipes/safe-content/safe-content.pipe';
import { ProfileComponent } from './profiles/profiles.component';

@NgModule({
  declarations: [
    AppComponent,
    FeedComponent,
    SignInComponent,
    SignUpComponent,
    SignOutComponent,
    PostComponent,
    SearchComponent,
    CreatePostComponent,
    PostDetailComponent,
    CommentGroupComponent,
    CommentComponent,
    CommentCreateComponent,
    CommentEditComponent,
    CommentFooterComponent,
    // CommentUserComponent,
    CommentListComponent,
    ConfirmationDialogComponent,
    SafeContentPipe
  ],
  entryComponents: [
    ConfirmationDialogComponent,
    // CommentUserComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    TimeSinceModule,
    FlexLayoutModule,
    ReactiveFormsModule,
    HttpClientModule,
    HttpClientXsrfModule.withOptions({
      cookieName: 'csrftoken',
      headerName: 'X-CSRFToken'
    }),
    BrowserAnimationsModule,
    CommonModule,
    TimeSinceModule,
    MaterialModule.forRoot(),
    FroalaViewModule.forRoot(),
    FroalaEditorModule,
    AppRoutingModule
  ],
  providers: [  CookieService,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true,
    },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: HttpXsrfInterceptor,
      multi: true
    },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
