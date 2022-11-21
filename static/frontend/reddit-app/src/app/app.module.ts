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
import { SearchComponent } from './components/search/search.component';

import { AuthInterceptor } from './auth.interceptor';
import { HttpXsrfInterceptor } from './auth.header.interceptor';

import { TimeSinceModule } from '@thisissoon/angular-timesince';
import { FroalaEditorModule, FroalaViewModule } from 'angular-froala-wysiwyg';
import { FlexLayoutModule } from '@angular/flex-layout';
import { SafeContentPipe } from '@reddit/core/pipes/safe-content/safe-content.pipe';

import { PostComponent } from './components/post/post.component';
import { CreatePostComponent } from './components/create-post/create-post.component';
import { PostDetailComponent } from './components/post-detail/post-detail.component';
import { PostLoaderComponent } from './components/post-loader/post-loader.component';


import { CommentGroupComponent } from './components/comment-group/comment-group.component';
import { CommentComponent } from './components/comment/comment.component';
import { CommentCreateComponent } from './components/comment-create/comment-create.component';
import { CommentEditComponent } from './components/comment-edit/comment-edit.component';
import { CommentFooterComponent } from './components/comment-footer/comment-footer.component';
import { CommentListComponent } from './components/comment-list/comment-list.component';
import { ConfirmationDialogComponent } from './components/confirmation-dialog/confirmation-dialog.component';

import { ProfileComponent } from './profiles/profiles/profiles.component';
import { AddInterestDialogComponent } from './profiles/add-interest-dialog/add-interest-dialog.component';
import { ProfileBookmarksComponent } from './profiles/profile-bookmarks/profile-bookmarks.component';
import { ProfileCommentsComponent } from './profiles/profile-comments/profile-comments.component';
import { ProfileUpvotesComponent } from './profiles/profile-upvotes/profile-upvotes.component';
import { ProfileDownvotesComponent } from './profiles/profile-downvotes/profile-downvotes.component';
import { ProfileHistoryComponent } from './profiles/profile-history/profile-history.component';
import { ProfileOverviewComponent } from './profiles/profile-overview/profile-overview.component';
import { ProfilePostsComponent } from './profiles/profile-posts/profile-posts.component';

import { GroupComponent } from './group/group/group.component';
import { GroupPostComponent } from './group/group-post/group-post.component';
import { GroupFeedComponent } from './group/group-feed/group-feed.component';
import { CreateGroupComponent } from './group/create-group/create-group.component';
import { GroupRouterComponent } from './group/group-router/group-router.component';

@NgModule({
  declarations: [
    AppComponent,
    FeedComponent,
    SignInComponent,
    SignUpComponent,
    SignOutComponent,

    PostComponent,
    CreatePostComponent,
    PostDetailComponent,
    PostLoaderComponent,

    SearchComponent,

    CommentGroupComponent,
    CommentComponent,
    CommentCreateComponent,
    CommentEditComponent,
    CommentFooterComponent,
    CommentListComponent,

    ConfirmationDialogComponent,

    GroupComponent,
    GroupPostComponent,
    GroupFeedComponent,
    CreateGroupComponent,
    GroupRouterComponent,

    AddInterestDialogComponent,
    ProfileComponent,
    ProfileOverviewComponent,
    ProfileBookmarksComponent,
    ProfilePostsComponent,
    ProfileHistoryComponent,
    ProfileUpvotesComponent,
    ProfileCommentsComponent,
    ProfileDownvotesComponent,

    SafeContentPipe
  ],
  entryComponents: [
    ConfirmationDialogComponent,
    AddInterestDialogComponent,
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
    FroalaEditorModule.forRoot(),
    AppRoutingModule,
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
